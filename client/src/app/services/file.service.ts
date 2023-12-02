import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { FileFlatNode, FileNode } from '@models/file-tree.model';

@Injectable({
  providedIn: 'root',
})
export class FileService {
  private baseUrl = 'http://127.0.0.1:5000';

  constructor(private http: HttpClient) {}

  getDirectoryStructure(): Observable<FileNode[]> {
    const url = `${this.baseUrl}/get_directory_structure`;
    return this.http.get<FileNode[]>(url);
  }

  convertToFullPath(node: FileFlatNode): string {
    const pathSegments: string[] = [];

    while (node) {
      pathSegments.unshift(node.name);
      node = node.parent!;
    }

    return pathSegments.join('/');
  }

  saveFile(filename: string, content: string): Observable<any> {
    const url = `${this.baseUrl}/save_file`;
    const data = { filename, content };
    return this.http.post(url, data);
  }
}