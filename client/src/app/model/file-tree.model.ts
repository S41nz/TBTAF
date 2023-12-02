export interface FileNode {
  name: string;
  type?: string; 
  children?: FileNode[];
}

export interface FileFlatNode {
  name: string;
  level: number;
  expandable: boolean;
  parent: FileFlatNode | null;
  type?: string;
  children?: FileNode[];
}

/** Flat node with expandable and level information */
export class FileFlatNode {
  constructor(
    public expandable: boolean,
    public name: string,
    public level: number,
    public type?: string 
  ) {}
}