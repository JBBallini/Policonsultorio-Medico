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
  responsable?: Responsable;
}

@Injectable({
  providedIn: 'root'
})
export class PacienteService {
  private apiUrl = 'http://127.0.0.1:8000/api/registro-paciente/';
  private apiUrl2 = 'http://127.0.0.1:8000/api/';

  constructor(private http: HttpClient) {}

  registrarPaciente(paciente: Paciente): Observable<any> {
    return this.http.post<any>(this.apiUrl, paciente);  
  }

  getPacientePorDni(dni: string): Observable<Paciente> {
    return this.http.get<Paciente>(`${this.apiUrl2}${dni}/`);
  }

}
