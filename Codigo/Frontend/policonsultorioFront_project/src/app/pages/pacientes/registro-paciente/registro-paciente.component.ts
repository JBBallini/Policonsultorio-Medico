import { Component } from '@angular/core';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { PacienteService } from '@app/services/paciente.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-registro-paciente',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, HttpClientModule],
  templateUrl: './registro-paciente.component.html',
  styleUrls: ['./registro-paciente.component.css']
})

//Se define la clase para el componente de Registro de Paciente
export class RegistroPacienteComponent {
  //Atributos
  pacienteForm: FormGroup;
  mostrarResponsable = false;
  mensaje: string | null = null;
  error: string | null = null;
  enviando = false;

  constructor(
    private fb: FormBuilder,
    private pacienteService: PacienteService,
    private router: Router
  ) {
    //Creamos el formulario
    this.pacienteForm = this.fb.group({
      dniPaciente: ['', Validators.required],
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      telefono: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      fechaNacimiento: ['', Validators.required],
      direccion: ['', Validators.required],
      tipoSangre: ['', Validators.required],
      responsable: this.fb.group({
        dniResponsable: [''],
        nombre: [''],
        apellido: [''],
        telefono: [''],
        email: [''],
        fechaNacimiento: [''],
        direccion: [''],
        tipoSangre: ['']
      })
    });
  }

  //Método que se utiliza para mostrar los campos del responsable en el HTML si el paciente es menor de edad
  alCambiarFechaNacimiento() {
    const fecha = new Date(this.pacienteForm.get('fechaNacimiento')?.value);
    const hoy = new Date();
    let edad = hoy.getFullYear() - fecha.getFullYear();
    const m = hoy.getMonth() - fecha.getMonth();
    if (m < 0 || (m === 0 && hoy.getDate() < fecha.getDate())) edad--;
    this.mostrarResponsable = edad < 18;
  }

  //Método para registrar al paciente
  registrarPaciente() {
    if (this.enviando) return;
    this.mensaje = null;
    this.error = null;

    //Obtenemos los datos cargados en el formulario y la fecha de actual
    const data = this.pacienteForm.value;
    const hoy = new Date();

    //Verificamos que la fecha de nacimiento no sea mayor a la fecha actual
    const fNac = new Date(data.fechaNacimiento);
    if (fNac > hoy) {
      this.error = 'La fecha de nacimiento del paciente no puede ser posterior a hoy.';
      return;
    }

    //El campo de responsable de paciente pasa a true si necesita responsable
    const edadPaciente = this.calcularEdad(fNac);
    this.mostrarResponsable = edadPaciente < 18;

    //Validaciones adicionales
    if (this.mostrarResponsable) {
      const r = data.responsable;

      //Se comprueba que todos los campos del responsable esten completos
      if (!r.dniResponsable || !r.nombre || !r.apellido || !r.fechaNacimiento) {
        this.error = 'Debe completar todos los campos del responsable.';
        return;
      }

      //Se verifica que el dni del responsable no sea igual al del paciente
      if (r.dniResponsable === data.dniPaciente) {
        this.error = 'El responsable no puede tener el mismo DNI que el paciente.';
        return;
      }

      //Se verifica que la fecha de nacimiento del responsable no sea mayor a la actual
      const fResp = new Date(r.fechaNacimiento);
      if (fResp > hoy) {
        this.error = 'La fecha de nacimiento del responsable no puede ser posterior a hoy.';
        return;
      }
    } else {
      //Si no es necesario el responsable en el paciente, lo elimina
      delete data.responsable;
    }

    //Se hace un POST en el back llamando al método del service para registrar al paciente con los datos cargados
    this.enviando = true;
    this.pacienteService.registrarPaciente(data).subscribe({
      next: (res) => {
        this.mensaje = res.message || 'Paciente registrado correctamente.';
        setTimeout(() => this.router.navigate(['/lista-de-Pacientes']), 1500);
      },
      error: (err) => {
        this.error =
          err.error?.error ||
          err.error?.detail ||
          'Error al registrar el paciente. Verifique los datos.';
        this.enviando = false;
      }
    });
  }

  //Método para calcular la edad del apciente
  private calcularEdad(fecha: Date): number {
    const hoy = new Date();
    let edad = hoy.getFullYear() - fecha.getFullYear();
    const m = hoy.getMonth() - fecha.getMonth();
    if (m < 0 || (m === 0 && hoy.getDate() < fecha.getDate())) edad--;
    return edad;
  }

  //Método del btn para volver a la lista de pacientes
  volverAListaDePacientes() {
    this.router.navigate(['/lista-de-Pacientes']);
  }
}
