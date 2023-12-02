import { Component, EventEmitter, Input, Output } from '@angular/core';
import {
  MatTreeFlatDataSource,
  MatTreeFlattener,
  MatTreeModule,
} from '@angular/material/tree';
import { MatIconModule } from '@angular/material/icon';
import { FlatTreeControl } from '@angular/cdk/tree';
import { FileFlatNode, FileNode } from '@models/file-tree.model';
import { Subscription } from 'rxjs'
import { FileService } from '@services/file.service';

@Component({
  selector: 'app-file-tree',
  standalone: true,
  imports: [MatTreeModule, MatIconModule],
  template: `
    <mat-tree [dataSource]="dataSource" [treeControl]="treeControl">
      <mat-tree-node *matTreeNodeDef="let node" matTreeNodePadding>
        <button mat-icon-button disabled>
          <mat-icon>{{ getIcon(node) }}</mat-icon>
        </button>
        {{ node.name }}
      </mat-tree-node>

      <mat-tree-node
        *matTreeNodeDef="let node; when: hasChild"
        matTreeNodePadding
        (click)="selectFile(node)"
        [style.padding-left]="getPadding(node)"
      >
        <button
          mat-icon-button
          [attr.aria-label]="'toggle ' + node.name"
          matTreeNodeToggle
        >
          <mat-icon class="mat-icon-rtl-mirror">
            {{ treeControl.isExpanded(node) ? 'expand_more' : 'chevron_right' }}
          </mat-icon>
        </button>
        <mat-icon>{{ getIcon(node) }}</mat-icon>
        {{ node.name }}
      </mat-tree-node>
    </mat-tree>
  `,
  styles: `
    button[mat-icon-button] {
      min-width: 24px;
    }
  `,
})
export class FileTreeComponent {
  @Input() directory = '';
  @Output() fileSelected: EventEmitter<FileFlatNode> = new EventEmitter<FileFlatNode>();

  treeControl = new FlatTreeControl<FileFlatNode>(
    (node) => node.level,
    (node) => node.expandable
  );

  treeFlattener = new MatTreeFlattener(
    this.transformerWithParent.bind(this), // Adjust the binding of the transformer function
    (node) => node.level,
    (node) => node.expandable,
    (node) => node.children
  );
  dataSource = new MatTreeFlatDataSource(this.treeControl, this.treeFlattener);
  private subscription = new Subscription();

  constructor(private fileService: FileService) {}

  ngOnInit() {
    this.subscription.add(
      this.fileService.getDirectoryStructure().subscribe({
        next: (data) =>  this.dataSource.data = this.buildFileTree(data, null),
        error: (error) => console.error('Error fetching directory structure:', error)
      })
    )
  }

  transformerWithParent(node: FileNode, level: number): FileFlatNode {
    const flatNode: FileFlatNode = {
      expandable: !!node.children && node.children.length > 0,
      name: node.name,
      level,
      type: node.type,
      parent: null,
    };

    return flatNode;
  }

  private buildFileTree(data: FileNode[], parent: FileFlatNode | null): FileFlatNode[] {
    return data.map((item) => {
      const node: FileFlatNode = this.transformerWithParent(item, (parent?.level || 0) + 1);
      node.parent = parent;

      if (item.children) {
        node.children = this.buildFileTree(item.children, node);
      }

      return node;
    });
  }

  hasChild = (_: number, node: FileFlatNode) => node.expandable;

  selectFile(node: FileFlatNode) {
    this.fileSelected.emit(node);
  }

  getIcon(node: FileFlatNode): string {
    return node.type === 'folder' ? 'folder' : 'insert_drive_file'; // Adjust icons based on file type
  }

  getPadding(node: FileFlatNode): string {
    return `${16 + node.level * 16}px`; // Adjust indentation based on the level
  }
}
