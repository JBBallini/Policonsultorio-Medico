import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';
import { MedicoService } from '../../../services/medico.service';

@Component({
  selector: 'app-editar-medico',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, HttpClientModule],
  templateUrl: './editar-medico.component.html',
  styleUrls: ['./editar-medico.component.css']
})

//Definimos la clase del módulo
export class EditarMedicoComponent implements OnInit {

  //Atributos
  medicoForm!: FormGroup;
  mensaje: string | null = null;
  error: string | null = null;
  dniOriginal!: string;

  //Constructor de dependencias
  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private medicoService: MedicoService
  ) {}

  ngOnInit() {
    /*
      Obtenemos los datos del médico a partir del path especificado y el DNI, creamos el formulario y lo cargamos con los datos
      traidos del backend
    */
    this.dniOriginal = this.route.snapshot.paramMap.get('dni')!;
    this.inicializarFormulario();
    this.cargarMedico();
  }

  //Creamos la estructura del formulario de edición
  inicializarFormulario() {
    //medicoForm es un objeto con todos los campos del formulario
    this.medicoForm = this.fb.group({
      //Campos del formulario
      dniMedico: ['', Validators.required],
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      telefono: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      especialidad: ['', Validators.required],
      matricula: ['', Validators.required],
      //Horarios se compone de un subformulario ya que poseen sus propios atributos
      horarios: this.fb.array([])
    });
  }

  //Getter para obtener los horarios
  get horarios(): FormArray {
    return this.medicoForm.get('horarios') as FormArray;
  }

  //Método para cargar los datos 
  cargarMedico() {
    //Se realiza petición al back para obtener los datos del médico con el DNI
    this.medicoService.obtenerMedicoPorDni(this.dniOriginal).subscribe({
      //Se cargan los datos traidos del back al formulario
      next: (data: any) => {
        this.medicoForm.patchValue({
          dniMedico: data.dniMedico,
          nombre: data.nombre,
          apellido: data.apellido,
          telefono: data.telefono,
          email: data.email,
          especialidad: data.especialidad,
          matricula: data.matricula
        });

        //Se eliminan los horarios previos y se agregan los nuevos del back
        this.horarios.clear();
        const horarios = Array.isArray(data.horarios) ? data.horarios : [];

        //Se arma el subformulario de horarios
        horarios.forEach((h: any) => {
          this.horarios.push(
            this.fb.group({
              diaSemana: [h.diaSemana || 'LUN', Validators.required],
              horaInicio: [h.horaInicio || '', Validators.required],
              horaFin: [h.horaFin || '', Validators.required]
            })
          );
        });
      },
      //Mensaje de error si falla la carga de datos
      error: (err) => {
        this.error = 'Error al cargar los datos del médico';
      }
    });
  }

  //Método para agregar nuevos horarios
  agregarHorario() {
    this.horarios.push(
      this.fb.group({
        diaSemana: ['LUN', Validators.required],
        horaInicio: ['', Validators.required],
        horaFin: ['', Validators.required]
      })
    );
  }

  //Método para eliminar horario
  eliminarHorario(i: number) {
    this.horarios.removeAt(i);
  }

  //Método para actualizar al médico con los datos del formulario
  actualizarMedico() {
    this.mensaje = null;
    this.error = null;

    const data = {
      ...this.medicoForm.value,
      horarios: this.horarios.value
    };

    //Llama al método "actualizarMedico" del service para realizar un PUT
    this.medicoService.actualizarMedico(this.dniOriginal, data).subscribe({
      //Mensaje y redirije a la lista de médicos
      next: (res) => {
        this.mensaje = 'Médico actualizado correctamente';
        setTimeout(() => this.router.navigate(['/lista-de-medicos']), 1500);
      },
      error: (err) => {
        console.error(err);
        this.error = err.error?.detail || 'Error al actualizar el médico';
      }
    });
  }

  //Método para volver a la lista de médicos
  volverALista() {
    this.router.navigate(['/lista-de-medicos']);
  }
}

