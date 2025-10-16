import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Responsable {
  dniResponsable: string;
  nombre: string;
  apellido: string;
  telefono: string;
  email: string;
  fechaNacimiento: string;
  direccion: string;
  tipoSangre: string;
}

export interface Paciente {
  dniPaciente: string;
  nombre: string;
  apellido: string;
  telefono: string;
  email: string;
  fechaNacimiento: string;
  direccion: string;
  tipoSangre: string;
  responsable?: Responsable | null;
}

@Injectable({ providedIn: 'root' })
export class PacienteService {
  private apiUrl = 'http://127.0.0.1:8000/api/pacientes/';

  constructor(private http: HttpClient) {}

  getPacientePorDni(dni: string): Observable<Paciente> {
    return this.http.get<Paciente>(`${this.apiUrl}${dni}/`);
  }

  getPacientes(): Observable<Paciente[]> {
    return this.http.get<Paciente[]>(this.apiUrl);
  }

  actualizarPaciente(dni: string, data: Partial<Paciente>): Observable<Paciente> {
    return this.http.put<Paciente>(`${this.apiUrl}${dni}/`, data);
  }

  eliminarPaciente(dni: string): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}${dni}/`);
  }
}

