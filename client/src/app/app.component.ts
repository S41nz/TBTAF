import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterOutlet } from '@angular/router';
import { EditorWindowComponent } from '@components/editor-window/editor-window.component';
import { FileTreeComponent } from '@components/file-tree/file-tree.component';
import { Tab, TabsComponent } from '@components/tabs/tabs.component';
import { TerminalComponent } from '@components/terminal/terminal.component';
import { Observable } from 'rxjs';
import { MainService } from '@services/main.service';
import { FileFlatNode } from '@models/file-tree.model';

@Component({
  selector: 'app-root',
  standalone: false,
  template: `
  <div class="app-container">
    <div class="sidebar">
      <app-file-tree (fileSelected)="onFileSelected($event)"></app-file-tree>
    </div>
    <div class="main-content">
      <app-tabs
        [tabs]="(openTabs$ | async) || []"
        [activeTabIndex]="(activeTabIndex$ | async) || 0"
        (tabChange)="onTabChange($event)"
        (tabClose)="onTabClose($event)"
      >
        <app-editor-window
          *ngFor="let tab of openTabs$ | async"
          [fileContent]="getFileContent(tab.title)"
        ></app-editor-window>
      </app-tabs>
    <app-terminal></app-terminal>
  </div>
</div>

  `,
  styles: `
    .app-container {
      display: grid;
      height: 100vh;
      width: 100vw;
      grid-template-areas: "sidebar main-content";
      grid-template-columns: 1fr 3fr;
    }

  .sidebar {
    grid-area: sidebar;
    height: 100%;
  }

  .main-content {
    grid-area: main-content;
    height: 100%;
    display: grid;
    grid-template-areas: "editor" "terminal";
    grid-template-rows: minmax(600px, 2fr) 1fr;
  }

  `,
})
export class AppComponent {
  openTabs$: Observable<Tab[]> = this.mainService.openTabs$;
  activeTabIndex$: Observable<number> = this.mainService.activeTabIndex$;

  constructor(private mainService: MainService) {}

  ngOnInit(): void {
    // Initial setup, e.g., load default file, open tabs, etc.
    this.mainService.addTab({ title: 'Default File' });
  }

  onFileSelected(fileName: FileFlatNode): void {
    const tab: Tab = { title: fileName.name };
    this.mainService.addTab(tab);
    this.mainService.setActiveTabIndex(
      this.mainService.openTabsSource.value.length - 1
    );
    this.getFileContent(tab.title)
  }

  onTabChange(index: number): void {
    this.mainService.setActiveTabIndex(index);
  }

  onTabClose(index: number): void {
    this.mainService.closeTab(index);
  }

  getFileContent(fileName: string): string {
    return `# Content of ${fileName} goes here`;
  }
}
