import { Component } from '@angular/core';
import { FormBuilder, FormGroup, FormArray, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { Router } from '@angular/router';
import { MedicoService } from '../../../services/medicoRegistro.service';

@Component({
  selector: 'app-registro-medico',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, HttpClientModule],
  templateUrl: './registro-medico.component.html',
  styleUrls: ['./registro-medico.component.css']
})

//Se define la clase para el registro médico
export class RegistroMedicoComponent {
  //Atributos
  medicoForm: FormGroup;
  mensaje: string | null = null;
  error: string | null = null;

  constructor(private fb: FormBuilder, private medicoService: MedicoService, private router: Router) {
    //Componentes del formulario de registro
    this.medicoForm = this.fb.group({
      dniMedico: ['', Validators.required],
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      telefono: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      especialidad: ['', Validators.required],
      matricula: ['', Validators.required],
      //Subformulario para horarios
      horarios: this.fb.array([])
    });
  }

  //Getter de los horarios
  get horarios(): FormArray {
    return this.medicoForm.get('horarios') as FormArray;
  }

  //Método para agregar horarios al médico
  agregarHorario() {
    //Se crea el nuevo subformulario para los horarios
    const nuevoHorario = this.fb.group({
      diaSemana: ['LUN', Validators.required],
      horaInicio: ['', Validators.required],
      horaFin: ['', Validators.required]
    });

    const horariosActuales = this.horarios.value;

    const diaNuevo = nuevoHorario.value.diaSemana;
    const inicioNuevo = nuevoHorario.value.horaInicio;
    const finNuevo = nuevoHorario.value.horaFin;

    //Hacemos la verificación de dias y horarios duplicados antes de ser registrado
    const existeDuplicado = horariosActuales.some(
      (h: any) =>
        h.diaSemana === diaNuevo &&
        h.horaInicio === inicioNuevo &&
        h.horaFin === finNuevo
    );

    if (existeDuplicado) {
      alert('Ya existe un horario con el mismo día y rango horario.');
      return;
    }

    this.horarios.push(nuevoHorario);
  }

  //Método apra eliminar horario
  eliminarHorario(i: number) {
    this.horarios.removeAt(i);
  }

  //Método apra registrar al médico
  registrarMedico() {
    this.mensaje = null;
    this.error = null;

    //Verifica que si hay al menos un horario
    if (this.horarios.length === 0) {
      this.error = 'Debe agregar al menos un horario';
      return;
    }

    //Llama al método de horarios dupplicados para verificación
    if (this.tieneHorariosDuplicados()) {
      this.error = 'No se puede registrar horarios repetidos';
      return;
    }

    //Se verifica que el horario Inicio < horario Fin
    const horariosInvalidos = this.horarios.value.filter((h: any) => {
      if (!h.horaInicio || !h.horaFin) return true;

      const [hInicio, mInicio] = h.horaInicio.split(':').map(Number);
      const [hFin, mFin] = h.horaFin.split(':').map(Number);
      const minutosInicio = hInicio * 60 + mInicio;
      const minutosFin = hFin * 60 + mFin;

      //Se comparan minutos entre ambos horarios
      return minutosInicio >= minutosFin;
    });

    //Se lanza error si encuentra horario Inicio > horario Fin
    if (horariosInvalidos.length > 0) {
      this.error = 'Hay horarios con hora de inicio igual o mayor a la hora de fin.';
      return;
    }

    const data = {
      ...this.medicoForm.value,
      horarios: this.horarios.value
    };

    //Si no se encuentra error, registra el médico llamando al service y haciendo un POST
    this.medicoService.registrarMedico(data).subscribe({
      next: (res) => {
        this.mensaje = res.message;
        setTimeout(() => this.router.navigate(['/lista-de-Medicos']), 1500);
      },
      error: (err) => {
        console.error('Error en registro:', err);
        this.error = err.error?.detail || 'Error al registrar el médico';
      }
    });
  }

  //Método para volver a la lista de médicos
  volverALista() {
    this.router.navigate(['/lista-de-medicos/']);
  }

  //Método para evitar que el médico tenga horarios duplicados o superpuestos
  tieneHorariosDuplicados(): boolean {
    //Set no permite elementos duplicados
    const combinaciones = new Set<string>();
    const horarios = this.horarios.value;

    for (let horario of horarios) {
      //A cada horario se le asigna una clave, si otro horario tiene la misma clave entonces son duplicados.
      const clave = `${horario.diaSemana}-${horario.horaInicio}-${horario.horaFin}`;
      if (combinaciones.has(clave)) {
        return true;
      }
      combinaciones.add(clave);
    }

    return false;
  }
}