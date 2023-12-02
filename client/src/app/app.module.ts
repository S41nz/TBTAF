import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { MatCommonModule } from '@angular/material/core';
import { EditorWindowComponent } from '@components/editor-window/editor-window.component';
import { FileTreeComponent } from '@components/file-tree/file-tree.component';
import { TabsComponent } from '@components/tabs/tabs.component';
import { TerminalComponent } from '@components/terminal/terminal.component';
import { MonacoEditorModule } from 'ngx-monaco-editor-v2';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MatCommonModule,
    EditorWindowComponent,
    FileTreeComponent,
    TabsComponent,
    TerminalComponent,
    MonacoEditorModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
