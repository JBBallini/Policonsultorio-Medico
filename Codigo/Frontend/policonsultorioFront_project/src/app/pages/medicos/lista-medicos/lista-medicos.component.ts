import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MedicoService } from '../../../services/medico.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-lista-medicos',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './lista-medicos.component.html',
  styleUrls: ['./lista-medicos.component.css']
})

//Se define la clase para la lista de Médicos
export class ListaMedicosComponent implements OnInit {
  //Atributos de la clase
  medicos: any[] = [];
  //Atributos del filtro de búsqueda por DNI
  medicosFiltrados: any[] = [];
  filtroDni: string = '';
  mensaje: string | null = null;

  constructor(private medicoService: MedicoService, private router: Router) {}

  //Al iniciar el componente se cargar los médicos
  ngOnInit(): void {
    this.cargarMedicos();
  }

  //Se le pide al service por medio de un GET para obtener los registros de los médicos y cargarlos
  cargarMedicos() {
    this.medicoService.obtenerMedicos().subscribe({
      next: (data) => {
        this.medicos = data;
        this.medicosFiltrados = data;
      },
      error: () => (this.mensaje = 'Error al cargar los médicos')
    });
  }

  //Método para filtrar los médicos por DNI
  filtrarMedicos() {
    //Se obtiene el dato cargado por el usuario
    const filtro = this.filtroDni.trim().toLowerCase();
    //Se recorre la lista de médicos y busca el del dni ingresado
    this.medicosFiltrados = this.medicos.filter(m =>
      m.dniMedico.toLowerCase().includes(filtro)
    );
  }

  //Método para eliminar un médico en la lista
  eliminarMedico(dni: string) {
    if (confirm('¿Seguro que deseas eliminar este médico?')) {
      //Llama al service para hacer un DELETE
      this.medicoService.eliminarMedico(dni).subscribe({
        next: () => {
          this.mensaje = 'Médico eliminado correctamente';
          this.cargarMedicos();
        },
        error: () => (this.mensaje = 'Error al eliminar el médico')
      });
    }
  }

  //Méotdo para ir a editar un médico
  editarMedico(dni: string) {
    this.router.navigate(['/editar-medico', dni]);
  }

  //Método para ir al registro de médicos
  irARegistro() {
    this.router.navigate(['/registro-medico']);
  }

  //Méotdo para volver al menú principal
  volver() {
    this.router.navigate(['']);
  }
}


