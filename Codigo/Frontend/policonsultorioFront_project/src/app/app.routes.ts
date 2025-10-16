import { Routes } from '@angular/router';
import { RegistroPacienteComponent } from './pages/pacientes/registro-paciente/registro-paciente.component';
import { EditarPacienteComponent } from './pages/pacientes/editar-paciente/editar-paciente.component';
import { ListaPacientesComponent } from './pages/pacientes/lista-pacientes/lista-pacientes.component';
import { RegistroMedicoComponent } from './pages/medicos/registro-medico/registro-medico.component';
import { ListaMedicosComponent } from './pages/medicos/lista-medicos/lista-medicos.component';
import { EditarMedicoComponent } from './pages/medicos/editar-medico/editar-medico.component';
import { RegistrarTurnoComponent } from './pages/turnos/registrar-turno/registrar-turno.component';
import { ListaTurnosComponent } from './pages/turnos/lista-turnos/lista-turnos.component';
import { EditarTurnoComponent } from './pages/turnos/editar-turno/editar-turno.component';
import { InicioComponent } from './pages/inicio/inicio';

export const routes: Routes = [
{ path: '', component: InicioComponent },
{ path: 'registro-paciente', component: RegistroPacienteComponent },
{ path: 'editar-paciente/:dni', component: EditarPacienteComponent },
{ path: 'lista-de-Pacientes', component: ListaPacientesComponent },
{ path: 'registro-medico', component: RegistroMedicoComponent },
{ path: 'lista-de-medicos', component: ListaMedicosComponent },
{ path: 'editar-medico/:dni', component: EditarMedicoComponent },
{ path: 'turnos/registrar-turno/:dni', component: RegistrarTurnoComponent },
{ path: 'lista-turnos', component: ListaTurnosComponent },
{ path: 'editar-turno/:id', component: EditarTurnoComponent },
];



