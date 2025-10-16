import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegistrarTurno } from './registrar-turno';

describe('RegistrarTurno', () => {
  let component: RegistrarTurno;
  let fixture: ComponentFixture<RegistrarTurno>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RegistrarTurno]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RegistrarTurno);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
