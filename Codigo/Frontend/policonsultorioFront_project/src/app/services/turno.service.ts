import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class TurnoService {
  private apiUrl = 'http://127.0.0.1:8000/api/turnos/';

  constructor(private http: HttpClient) {}

  obtenerTurnos(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }

  obtenerTurno(id: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}${id}/`);
  }

  eliminarTurno(id: number): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${id}/`);
  }

  actualizarTurno(id: number, data: any): Observable<any> {
    return this.http.patch<any>(`${this.apiUrl}${id}/`, data);
  }


  obtenerDisponibilidad(dniMedico: string, fecha: string): Observable<any> {
    return this.http.get(`${this.apiUrl}disponibilidad/?medico=${dniMedico}&fecha=${fecha}`);
  }
}

