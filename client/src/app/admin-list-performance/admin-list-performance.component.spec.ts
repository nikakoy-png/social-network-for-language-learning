import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminListPerformanceComponent } from './admin-list-performance.component';

describe('AdminListPerformanceComponent', () => {
  let component: AdminListPerformanceComponent;
  let fixture: ComponentFixture<AdminListPerformanceComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AdminListPerformanceComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AdminListPerformanceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
