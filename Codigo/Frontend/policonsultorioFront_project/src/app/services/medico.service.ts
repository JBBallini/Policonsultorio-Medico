import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class MedicoService {
  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  obtenerMedicos(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/medicos/`);
  }

  eliminarMedico(dni: string): Observable<any> {
    return this.http.delete(`${this.apiUrl}/medicos/${dni}/`);
  }

  obtenerMedicoPorDni(dni: string) {
    return this.http.get(`${this.apiUrl}/medicos/${dni}/`);
  }

  actualizarMedico(dni: string, data: any) {
    return this.http.put(`${this.apiUrl}/medicos/${dni}/`, data);
  }
}