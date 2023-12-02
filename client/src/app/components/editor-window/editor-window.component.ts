import { Component, Input } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { FileFlatNode } from '@models/file-tree.model';
import { FileService } from '@services/file.service';
import { MonacoEditorModule } from 'ngx-monaco-editor-v2';
import { Subscription } from 'rxjs'

@Component({
  selector: 'app-editor-window',
  standalone: true,
  imports: [MonacoEditorModule, FormsModule],
  providers: [],
  template: `
    <ngx-monaco-editor
      [options]="editorOptions"
      [(ngModel)]="codeContent"
      (onInit)="editorInit($event)"
      class="editor-component"
    ></ngx-monaco-editor>
  `,
  styles: `
    .editor-component {
      min-height: 600px;
      .editor-container {
        height: 100%;
      }
    }
  `
})
export class EditorWindowComponent {
  @Input() fileContent: string = '';

  codeContent: string = 'function x() {\nconsole.log("Hello world!");\n}';
  editorOptions = {
    theme: 'vs-dark',
    language: 'python',
    automaticLayout: true,
  };

  constructor(private fileService: FileService) {}
  private subscription = new Subscription()

  editorInit(editor: any): void {

  }

  saveFile(node: FileFlatNode): void {
    const fullPath = this.fileService.convertToFullPath(node);
    const content = 'Your file content goes here.';
    
    this.subscription.add(
      this.fileService.saveFile(fullPath, content).subscribe({
        next: (next: any) => console.log('File saved successfully:', next),
        error: (error) => console.error('Error saving file:', error)
      })
    );
  }

}
