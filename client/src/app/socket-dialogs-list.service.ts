import { Injectable } from '@angular/core';
import {WebSocketSubject} from "rxjs/internal/observable/dom/WebSocketSubject";

@Injectable({
  providedIn: 'root'
})
export class SocketDialogsListService {
  private socket: WebSocket | null = null;

  connectToSocketServer(socketUrl: string): void {
    this.socket = new WebSocket(socketUrl);

    this.socket.onopen = event => {
      console.log('WebSocket connection opened:', event);
    };

    this.socket.onmessage = event => {
      console.log('WebSocket message received:', event.data);
    };

    this.socket.onclose = event => {
      console.log('WebSocket connection closed:', event);
    };
  }

  disconnectFromSocketServer(): void {
    if (this.socket) {
      this.socket.close();
      this.socket = null;
    }
  }

  onMessageReceived(callback: (msg: any) => void): void {
    if (this.socket) {
      this.socket.onmessage = event => {
        callback(event.data);
      };
    }
  }

}
