import { Injectable } from '@angular/core';
import { Tab } from '@components/tabs/tabs.component';
import { BehaviorSubject } from 'rxjs'

@Injectable({
  providedIn: 'root'
})
export class MainService {
  selectedFileSource = new BehaviorSubject<string>('');
  selectedFile$ = this.selectedFileSource.asObservable();

  openTabsSource = new BehaviorSubject<Tab[]>([]);
  openTabs$ = this.openTabsSource.asObservable();

  activeTabIndexSource = new BehaviorSubject<number>(0);
  activeTabIndex$ = this.activeTabIndexSource.asObservable();

  constructor() {}

  selectFile(fileName: string): void {
    this.selectedFileSource.next(fileName);
  }

  addTab(tab: Tab): void {
    const openTabs = this.openTabsSource.value;
    this.openTabsSource.next([...openTabs, tab]);
  }

  closeTab(index: number): void {
    const openTabs = this.openTabsSource.value;
    openTabs.splice(index, 1);
    this.openTabsSource.next([...openTabs]);

    const activeTabIndex = this.activeTabIndexSource.value;
    if (index === activeTabIndex && openTabs.length > 0) {
      this.activeTabIndexSource.next(0);
    }
  }

  setActiveTabIndex(index: number): void {
    this.activeTabIndexSource.next(index);
  }
}
