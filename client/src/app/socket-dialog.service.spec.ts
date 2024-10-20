import { TestBed } from '@angular/core/testing';

import { SocketDialogService } from './socket-dialog.service';

describe('SocketDialogService', () => {
  let service: SocketDialogService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SocketDialogService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
