import { TestBed } from '@angular/core/testing';

import { SocketDialogsListService } from './socket-dialogs-list.service';

describe('SocketDialogsListService', () => {
  let service: SocketDialogsListService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(SocketDialogsListService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
