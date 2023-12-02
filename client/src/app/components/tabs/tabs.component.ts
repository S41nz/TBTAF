import { Component, Input, Output, EventEmitter } from '@angular/core';
import { MatIconModule } from '@angular/material/icon';
import { MatTabsModule } from '@angular/material/tabs';

export interface Tab {
  id?: number;
  title: string;
}

@Component({
  selector: 'app-tabs',
  standalone: true,
  imports: [MatTabsModule, MatIconModule],
  template: `
    <mat-tab-group
      [selectedIndex]="activeTabIndex"
      (selectedTabChange)="tabChanged($event)"
    >
      @for(tab of tabs; track tab.title; let i = $index) {
        <mat-tab  [label]="tab.title">
        <ng-template matTabContent>
          @if(i === activeTabIndex) {
            <ng-content></ng-content>
          }
        </ng-template>
        <button mat-icon-button (click)="closeTab(i)" class="close-button">
          <mat-icon aria-label="Close tab">close</mat-icon>
        </button>
      </mat-tab>
      }
      
    </mat-tab-group>
  `,
  styles: `
    .close-button {
      position: absolute;
      top: 8px;
      right: 8px;
    }
    :host mat-tab-group {
      position: relative;
      height: 100%;
    }
  `
})
export class TabsComponent {
  @Input() tabs: Tab[] = [];
  @Input() activeTabIndex: number = 0;
  @Output() tabChange: EventEmitter<number> = new EventEmitter<number>();
  @Output() tabClose: EventEmitter<number> = new EventEmitter<number>();

  tabChanged(event: any): void {
    this.activeTabIndex = event.index;
    this.tabChange.emit(this.activeTabIndex);
  }

  closeTab(index: number): void {
    this.tabClose.emit(index);
  }
}
