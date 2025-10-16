import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule, FormBuilder, FormGroup, Validators } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { TurnoService } from '../../../services/turno.service';
import { MedicoService } from '../../../services/medico.service';

@Component({
  selector: 'app-editar-turno',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, HttpClientModule, RouterModule],
  templateUrl: './editar-turno.component.html',
  styleUrls: ['./editar-turno.component.css']
})

//Definimos la clase del componente
export class EditarTurnoComponent implements OnInit {
  //Atributos
  form!: FormGroup;
  id!: number;
  mensaje = '';
  error = '';
  horariosDisponibles: string[] = [];

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private turnoService: TurnoService,
    private medicoService: MedicoService
  ) {}

//Método que se usa al cargar el componente
ngOnInit() {
  //Obtenemos el turno por el id por URL
  this.id = Number(this.route.snapshot.paramMap.get('id'));
  //Creamos el formulario con los datos que tendrá el turno
  this.form = this.fb.group({
    fecha: ['', Validators.required],
    hora: ['', Validators.required],
    dniPaciente: [{ value: '', disabled: true }],
    dniMedico: [{ value: '', disabled: true }],
    estadoAsistencia: [{ value: '', disabled: true }]
  });


  //Hacemos un GET al back para obtener el turno desde el ID obtenido
  this.turnoService.obtenerTurno(this.id).subscribe({
    next: (t) => {
      //Obtenemos el dni del paciente y del médico
      const dniPac = t.dniPaciente?.dniPaciente || t.dniPaciente;
      const dniMed = t.dniMedico?.dniMedico || t.dniMedico;
      //Cargamos los datos obtenidos en el formulario anterior
      this.form.patchValue({
        dniPaciente: dniPac,
        dniMedico: dniMed,
        estadoAsistencia: t.estadoAsistencia ? 'Asistió' : 'No asistió',
        fecha: '',
        hora: ''
      });
    },
    error: () => (this.error = 'Error al cargar el turno')
  });
}

  //Método para conocer los horarios disponibles del médico
  cargarHorariosDisponibles() {
    //Tomamos los datos del formulario
    const { dniMedico, fecha } = this.form.getRawValue();
    if (!dniMedico || !fecha) return;

    //Llamamos al método del service para conocer la disponibilidad del médico en una fecha
    this.turnoService.obtenerDisponibilidad(dniMedico, fecha).subscribe({
      next: (res) => {
        //Guardamos los horarios obtenidos
        this.horariosDisponibles = res.disponibles;
        this.error = '';
      },
      error: (err) => {
        this.error = err.error?.error || 'Error al obtener horarios disponibles';
        this.horariosDisponibles = [];
      }
    });
  }

  //Método del guardado de la edición
  guardar() {
    //Comprobamos que los campos esten completos
    if (this.form.invalid) {
      this.error = 'Completa todos los campos obligatorios';
      return;
    }

    //obtenemos la fecha y hora del formulario
    const { fecha, hora } = this.form.getRawValue();
    //Llamamos al back mediante el service para hacer el PATCH en el turno
    this.turnoService.actualizarTurno(this.id, { fecha, hora }).subscribe({
      next: () => {
        this.mensaje = 'Turno actualizado correctamente';
        setTimeout(() => this.router.navigate(['/turnos/lista']), 1200);
      },
      error: (err) => (this.error = err.error?.error || 'Error al actualizar el turno')
    });
  }

  //Método del btn volver a la lista de turnos
  volver() {
    this.router.navigate(['/lista-turnos']);
  }
}


