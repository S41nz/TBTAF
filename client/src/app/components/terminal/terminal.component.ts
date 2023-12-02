import { Component } from '@angular/core';

@Component({
  selector: 'app-terminal',
  standalone: true,
  imports: [],
  template: `
    <p>
      terminal works!
    </p>
  `,
  styles: ``
})
export class TerminalComponent {
  // command: string = '';
  // output: string = '';

  // constructor(private terminalService: TerminalService) {}

  // ngOnInit() {}

  // runCommand() {
  //   // Sanitize input (implement proper sanitation)
  //   const sanitizedCommand = this.sanitizeInput(this.command);
    
  //   // Call Flask server
  //   this.terminalService.runCommand(sanitizedCommand).subscribe(
  //     (response) => {
  //       this.output = response;
  //     },
  //     (error) => {
  //       console.error('Error:', error);
  //     }
  //   );
  // }

  // sanitizeInput(input: string): string {
  //   // Implement input sanitation logic
  //   return input;
  // } 
}
