import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EditarTurno } from './editar-turno';

describe('EditarTurno', () => {
  let component: EditarTurno;
  let fixture: ComponentFixture<EditarTurno>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EditarTurno]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EditarTurno);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
