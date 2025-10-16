import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { Router, RouterModule } from '@angular/router';
import { TurnoService } from '../../../services/turno.service';

@Component({
  selector: 'app-lista-turnos',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, HttpClientModule, RouterModule],
  templateUrl: './lista-turnos.component.html',
  styleUrls: ['./lista-turnos.component.css']
})

//Definimos la clase
export class ListaTurnosComponent implements OnInit {
  //Atributos
  turnos: any[] = [];
  filtrados: any[] = [];
  form!: FormGroup;
  mensaje = '';
  cargando = true;

  constructor(private turnoService: TurnoService, private fb: FormBuilder, private router: Router) {}

  ngOnInit() {
    //Filtro de busqueda vacío
    this.form = this.fb.group({ dni: [''] });
    //Cargamos los turnos llamando al método
    this.cargarTurnos();
  }

  //Método para cargar los turnos
  cargarTurnos() {
    this.cargando = true;
    //Obtenemos los turnos llamando al service y haciendo un GET al back
    this.turnoService.obtenerTurnos().subscribe({
      next: (data) => {
        this.turnos = data;
        this.filtrados = data;
        this.cargando = false;
      },
      error: () => {
        this.mensaje = 'Error al cargar los turnos';
        this.cargando = false;
      }
    });
  }

  //Método para filtrar los turnos por el dni del paciente
  filtrar() {
    //Obtenemos el dato cargado en el campo
    const dni = (this.form.value.dni || '').trim();
    //SI esta vacío, cargamos todos los turnos
    if (!dni) {
      this.filtrados = this.turnos;
      return;
    }
    //Sino se cargan los turnos que coincidan con el DNI
    this.filtrados = this.turnos.filter(t => String(t.dniPaciente).includes(dni) || String(t.dniPaciente?.dniPaciente).includes(dni));
  }

  //Método del btn limpiar campo del filtro
  limpiar() {
    this.form.reset({ dni: '' });
    this.filtrados = this.turnos;
  }

  //Método del btn eliminar turno
  eliminar(id: number) {
    //Preguntamos si quiere eliminar el turno
    if (!confirm('¿Eliminar este turno?')) return;
    //Llamamos al service y hacemos un DELETE en el back a partir del id del turno
    this.turnoService.eliminarTurno(id).subscribe({
      next: () => {
        this.mensaje = 'Turno eliminado';
        this.cargarTurnos();
      },
      error: () => this.mensaje = 'Error al eliminar el turno'
    });
  }

  //Método del btn editar
  editar(id: number) {
    this.router.navigate(['/editar-turno', id]);
  }

  //Método del btn volver al inicio
  volver() {
    this.router.navigate(['']);
  }
}

