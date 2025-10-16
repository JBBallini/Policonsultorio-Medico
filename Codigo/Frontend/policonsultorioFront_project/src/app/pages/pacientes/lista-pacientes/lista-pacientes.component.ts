import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { RouterModule, Router } from '@angular/router';
import { PacienteService } from '@app/services/paciente2.service';

@Component({
  selector: 'app-lista-pacientes',
  standalone: true,
  templateUrl: './lista-pacientes.component.html',
  styleUrls: ['./lista-pacientes.component.css'],
  imports: [CommonModule, ReactiveFormsModule, HttpClientModule, RouterModule]
})

//Se define la clase para el componente de la lista de pacientes
export class ListaPacientesComponent implements OnInit {
  pacientes: any[] = [];
  buscadorForm!: FormGroup;
  mensaje = '';
  cargando = true;

  constructor(private pacienteService: PacienteService, private fb: FormBuilder, private router: Router) {}

  //Al iniciar el componente se carga una tabla vacía y se llama al método para cargar los pacientes
  ngOnInit() {
    this.buscadorForm = this.fb.group({
      dni: ['']
    });
    this.cargarPacientes();
  }

  //Método para cargar los pacientes
  cargarPacientes() {
    this.cargando = true;
    //Hacemos un GET al back para traer a los pacientes y guardarlos en una lista "pacientes"
    this.pacienteService.getPacientes().subscribe({
      next: (data) => {
        this.pacientes = data;
        this.cargando = false;
      },
      error: (err) => {
        console.error(err);
        this.mensaje = 'Error al cargar pacientes.';
        this.cargando = false;
      }
    });
  }

  //Método para filtrar a los pacientes por DNI
  buscarPorDni() {
    //Campo donde se ingresa el dni
    const dni = this.buscadorForm.value.dni.trim();
    //Si esta vacío, carga todos los empleados
    if (!dni) {
      //Si el buscador está vacío, entonces muestra todos los pacientes
      this.cargarPacientes(); 
      return;
    }
    //Sino carga el paciente con el dni correspondiente haciendo un GET al back
    this.pacienteService.getPacientePorDni(dni).subscribe({
      next: (paciente) => {
        //Si esta el paciente, retorna un array de un elemento
        this.pacientes = paciente ? [paciente] : [];
      },
      error: (err) => {
        console.warn('Paciente no encontrado:', err);
        this.pacientes = [];
        this.mensaje = 'No se encontró ningún paciente con ese DNI.';
      }
    });
  }

  eliminarPaciente(dni: string) {
    //Se le pregunta con un pop-up al usuario si quiere eliminar al paciente
    if (confirm(`¿Seguro que deseas eliminar al paciente con DNI ${dni}?`)) {
      //Llamamos al service y hacemos un DELETE en el back
      this.pacienteService.eliminarPaciente(dni).subscribe({
        //Si se eliminó correctamente, volvemos a cargar los pacientes
        next: () => {
          this.mensaje = 'Paciente eliminado correctamente.';
          this.cargarPacientes();
        },
        error: (err) => {
          console.error(err);
          this.mensaje = 'Error al eliminar el paciente.';
        }
      });
    }
  }

  //Método del btn para crear un turno en el paciente seleccionado
  crearTurno(dni: string) {
    this.router.navigate(['/turnos/registrar-turno', dni]);
  }

  //Método del btn para volver al inicio
  volver() {
    this.router.navigate(['']);
  }
}

