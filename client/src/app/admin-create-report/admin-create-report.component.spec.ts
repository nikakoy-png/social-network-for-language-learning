import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminCreateReportComponent } from './admin-create-report.component';

describe('AdminCreateReportComponent', () => {
  let component: AdminCreateReportComponent;
  let fixture: ComponentFixture<AdminCreateReportComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AdminCreateReportComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AdminCreateReportComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
