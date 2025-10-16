import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MedicoService {
  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  registrarMedico(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/registro-medico/`, data);
  }

  obtenerMedicos(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/medicos/`);
  }
}
