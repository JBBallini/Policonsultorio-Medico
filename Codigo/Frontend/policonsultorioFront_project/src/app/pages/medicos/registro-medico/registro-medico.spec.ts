import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RegistroMedico } from './registro-medico';

describe('RegistroMedico', () => {
  let component: RegistroMedico;
  let fixture: ComponentFixture<RegistroMedico>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RegistroMedico]
    })
    .compileComponents();

    fixture = TestBed.createComponent(RegistroMedico);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
