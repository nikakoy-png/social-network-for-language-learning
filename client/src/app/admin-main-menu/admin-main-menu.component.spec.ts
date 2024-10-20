import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminMainMenuComponent } from './admin-main-menu.component';

describe('AdminMainMenuComponent', () => {
  let component: AdminMainMenuComponent;
  let fixture: ComponentFixture<AdminMainMenuComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AdminMainMenuComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AdminMainMenuComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
