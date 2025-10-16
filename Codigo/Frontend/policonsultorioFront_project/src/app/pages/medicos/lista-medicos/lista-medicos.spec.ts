import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListaMedicos } from './lista-medicos';

describe('ListaMedicos', () => {
  let component: ListaMedicos;
  let fixture: ComponentFixture<ListaMedicos>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListaMedicos]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ListaMedicos);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
