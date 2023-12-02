import { ApplicationConfig } from '@angular/core';

import { provideAnimations } from '@angular/platform-browser/animations';
import { MonacoEditorModule } from 'ngx-monaco-editor-v2';

export const appConfig: ApplicationConfig = {
  providers: [provideAnimations(), { provide: MonacoEditorModule }],
};
