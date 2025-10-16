import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';
import { ActivatedRoute, Router } from '@angular/router';
import { TurnoService } from '../../../services/turnoRegistro.service';
import { PacienteService, Paciente } from '../../../services/paciente2.service';
import { MedicoService } from '../../../services/medico.service';

@Component({
  selector: 'app-crear-turno',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, HttpClientModule],
  templateUrl: './registrar-turno.component.html',
  styleUrls: ['./registrar-turno.component.css']
})

//Definimos la clase del componente
export class RegistrarTurnoComponent implements OnInit {
  //Atributos
  turnoForm!: FormGroup;
  paciente: Paciente | null = null;
  especialidades: string[] = [];
  medicos: any[] = [];
  medicosFiltrados: any[] = [];
  horariosDisponibles: string[] = [];
  mensaje: string | null = null;
  error: string | null = null;

  constructor(
    private fb: FormBuilder,
    private route: ActivatedRoute,
    private router: Router,
    private turnoService: TurnoService,
    private pacienteService: PacienteService,
    private medicoService: MedicoService
  ) {}

  //Método que se ejecuta al iniciar el componente
  ngOnInit() {
    //Tomamos el dni del paciente de la URL
    const dni = this.route.snapshot.paramMap.get('dni')!;
    //Llamamos al método para iniciar el formulario
    this.inicializarFormulario();

    //Obtenemos los datos del paciente por dni mediante un GET al back
    this.pacienteService.getPacientePorDni(dni).subscribe({
      //Cargamos los datos necesarios en el formulario con los datos obtenidos del paciente
      next: (p: Paciente) => {
        this.paciente = p;
        this.turnoForm.patchValue({
          dniPaciente: p.dniPaciente,
          nombrePaciente: `${p.nombre} ${p.apellido}`
        });
      },
      error: () => (this.error = 'Error al cargar datos del paciente')
    });

    //Llamamos a este método para obtener las especialidades disponibles en el policonsultorio
    this.cargarEspecialidades();
  }

  //Método que crea el formulario
  inicializarFormulario() {
    this.turnoForm = this.fb.group({
      dniPaciente: [''],
      nombrePaciente: [''],
      especialidad: ['', Validators.required],
      dniMedico: ['', Validators.required],
      fecha: ['', Validators.required],
      hora: ['', Validators.required],
      monto: [1000, Validators.required]
    });
  }

  //Método que obtiene las especialidades de todos los médicos
  cargarEspecialidades() {
    this.medicoService.obtenerMedicos().subscribe({
      next: (data: any[]) => {
        this.medicos = data;
        this.especialidades = [...new Set(data.map((m: any) => m.especialidad))];
      },
      error: () => (this.error = 'Error al cargar las especialidades')
    });
  }

  //Método usado para obtener una lista de médicos que corresponda a la especialidad seleccionada
  filtrarMedicosPorEspecialidad() {
    const esp = this.turnoForm.value.especialidad;
    this.medicosFiltrados = this.medicos.filter((m: any) => m.especialidad === esp);
    //Limpiamos los campos para volver a elegirlos
    this.turnoForm.patchValue({ dniMedico: '', hora: '' });
    this.horariosDisponibles = [];
  }

  //Método para obtener los horarios disponibles del médico seleccionado en la fecha elegida
  cargarHorariosDisponibles() {
    //Obtenemos los datos de los campos del formulario
    const dniMedico = this.turnoForm.value.dniMedico;
    const fecha = this.turnoForm.value.fecha;
    if (!dniMedico || !fecha) return;

    //Llamamos al service para obtener los horarios a partir del dni del médico y una fecha
    this.turnoService.obtenerDisponibilidad(dniMedico, fecha).subscribe({
      next: (res: any) => (this.horariosDisponibles = res.disponibles),
      error: (err) => (this.error = err.error?.error || 'Error al obtener horarios')
    });
  }

  //Método que crea el turno comprueba
  crearTurno() {
    //Comprueba si todos los campos fueron completados antes de registrar el turno
    if (this.turnoForm.invalid) {
      this.error = 'Completa todos los campos obligatorios';
      return;
    }

    //Obtenemos los datos del formulario
    const data = {
      fecha: this.turnoForm.value.fecha,
      hora: this.turnoForm.value.hora,
      dniPaciente: this.turnoForm.value.dniPaciente,
      dniMedico: this.turnoForm.value.dniMedico,
      monto: this.turnoForm.value.monto
    };

    //Hacemos el POST en el back mediante el service
    this.turnoService.crearTurno(data).subscribe({
      next: () => {
        this.mensaje = 'Turno creado correctamente';
        setTimeout(() => this.router.navigate(['/lista-de-Pacientes']), 1500);
      },
      error: (err) => (this.error = err.error?.error || 'Error al crear el turno')
    });
  }

  //Método del btn para volver a la lista de pacientes
  volver() {
    this.router.navigate(['/lista-de-Pacientes']);
  }
}
