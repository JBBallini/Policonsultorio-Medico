import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TurnoService {
  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  crearTurno(data: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/registro-turno/`, data);
  }

  obtenerDisponibilidad(dniMedico: string, fecha: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/turnos/disponibilidad/?medico=${dniMedico}&fecha=${fecha}`);
  }
}
