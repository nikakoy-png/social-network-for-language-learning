import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NoLanguagesUserComponent } from './no-languages-user.component';

describe('NoLanguagesUserComponent', () => {
  let component: NoLanguagesUserComponent;
  let fixture: ComponentFixture<NoLanguagesUserComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NoLanguagesUserComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(NoLanguagesUserComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
