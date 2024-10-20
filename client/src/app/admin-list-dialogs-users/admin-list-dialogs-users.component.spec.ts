import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminListDialogsUsersComponent } from './admin-list-dialogs-users.component';

describe('AdminListDialogsUsersComponent', () => {
  let component: AdminListDialogsUsersComponent;
  let fixture: ComponentFixture<AdminListDialogsUsersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AdminListDialogsUsersComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AdminListDialogsUsersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
