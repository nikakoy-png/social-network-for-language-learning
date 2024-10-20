import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ShowFeedbackDialogComponent } from './show-feedback-dialog.component';

describe('ShowFeedbackDialogComponent', () => {
  let component: ShowFeedbackDialogComponent;
  let fixture: ComponentFixture<ShowFeedbackDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ShowFeedbackDialogComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ShowFeedbackDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
