import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MoreDetailsUserComponent } from './more-details-user.component';

describe('MoreDetailsUserComponent', () => {
  let component: MoreDetailsUserComponent;
  let fixture: ComponentFixture<MoreDetailsUserComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MoreDetailsUserComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(MoreDetailsUserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
