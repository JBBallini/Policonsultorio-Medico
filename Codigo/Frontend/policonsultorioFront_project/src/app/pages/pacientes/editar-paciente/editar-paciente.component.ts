import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { PacienteService } from '@app/services/paciente2.service';

@Component({
  selector: 'app-editar-paciente',
  standalone: true,
  templateUrl: './editar-paciente.component.html',
  styleUrls: ['./editar-paciente.component.css'],
  imports: [CommonModule, ReactiveFormsModule, HttpClientModule]
})

//Se define la clase del componente
export class EditarPacienteComponent implements OnInit {
  //Atributos
  pacienteForm!: FormGroup;
  responsableForm!: FormGroup;
  dniPaciente!: string;
  mensaje = '';
  error = '';
  cargando = true;
  tieneResponsable = false;

  constructor(
    private route: ActivatedRoute,
    private fb: FormBuilder,
    private router: Router,
    private pacienteService: PacienteService
  ) {}

  //Al cargar el componente se obtiene los datos del paciente por DNI, se inicializa el formulario y se cargan los datos
  ngOnInit() {
    this.dniPaciente = this.route.snapshot.paramMap.get('dni')!;
    this.inicializarFormularios();
    this.cargarPaciente();
  }

  inicializarFormularios() {
    //Se crea el formulario del paciente
    this.pacienteForm = this.fb.group({
      dniPaciente: ['', Validators.required],
      nombre: ['', Validators.required],
      apellido: ['', Validators.required],
      telefono: [''],
      email: ['', [Validators.email]],
      fechaNacimiento: ['', Validators.required],
      direccion: [''],
      tipoSangre: ['']
    });

    //Se crea el formulario del responsable
    this.responsableForm = this.fb.group({
      dniResponsable: [''],
      nombre: [''],
      apellido: [''],
      telefono: [''],
      email: ['', [Validators.email]],
      fechaNacimiento: [''],
      direccion: [''],
      tipoSangre: ['']
    });
  }

  //Método para cargar los datos del paciente
  cargarPaciente() {
    //Hacemos un GET para obtener al paciente por medio de su DNI
    this.pacienteService.getPacientePorDni(this.dniPaciente).subscribe({
      next: (data: any) => {
        this.pacienteForm.patchValue(data);

        //Se el paciente tiene responsable, se cargan los datos del responsable
        if (data.responsable) {
          this.tieneResponsable = true;
          this.responsableForm.patchValue(data.responsable);
        }
        //Prueba boton eliminar responsable
        this.verificarEdadParaResponsable();
        this.cargando = false;
      },
      error: (error) => {
        console.error(error);
        this.error = 'Error al cargar los datos del paciente.';
        this.cargando = false;
      }
    });
  }

  //Método para verificar la edad del responsable
  verificarEdadParaResponsable() {
    const fechaNacimiento = new Date(this.pacienteForm.get('fechaNacimiento')?.value);
    const hoy = new Date();
    let edad = hoy.getFullYear() - fechaNacimiento.getFullYear();
    const m = hoy.getMonth() - fechaNacimiento.getMonth();
    if (m < 0 || (m === 0 && hoy.getDate() < fechaNacimiento.getDate())) edad--;
  }

  //Método para actualizar el paciente
  actualizarPaciente() {
    this.error = '';

    //Obtenemos los datos del paciente y el responsable
    const datosPaciente = this.pacienteForm.getRawValue();
    const datosResponsable = this.responsableForm.value;

    //Validaciones para las fechas
    const hoy = new Date();
    const fechaNacPaciente = new Date(datosPaciente.fechaNacimiento);

    //Verficamos que la fechaNac del paciente no sea mayor a la actual
    if (fechaNacPaciente > hoy) {
      this.error = 'La fecha de nacimiento no puede ser posterior a hoy.';
      return;
    }

    //Calculamos la edad del paciente
    const edad = hoy.getFullYear() - fechaNacPaciente.getFullYear() - 
      ((hoy.getMonth() < fechaNacPaciente.getMonth()) || 
      (hoy.getMonth() === fechaNacPaciente.getMonth() && hoy.getDate() < fechaNacPaciente.getDate()) ? 1 : 0);

    //Si el paciente es menor de edad, se le debe asignar un responsable
    if (edad < 18 && !this.tieneResponsable) {
      this.error = 'Los pacientes menores de edad deben tener un responsable.';
      return;
    }

    //Guardamos los datos del responsable
    const payload = {
      ...datosPaciente,
      responsable: this.tieneResponsable ? datosResponsable : null
    };

    //Si pasa las validaciones, se hace un PUT llamando al service
    this.pacienteService.actualizarPaciente(this.dniPaciente, payload).subscribe({
      next: () => {
        this.mensaje = 'Datos actualizados correctamente.';
        setTimeout(() => this.router.navigate(['/lista-de-Pacientes']), 1500);
      },
      error: (error) => {
        console.error('Error al actualizar:', error);
        this.error = error.error?.error || 'Error al actualizar los datos.';
      }
    });
  }

  //Método para volver a la lista de pacientes
  volverAListaDePacientes() {
    this.router.navigate(['/lista-de-Pacientes']);
  }
}


