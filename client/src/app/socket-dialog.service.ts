import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class SocketDialogService {

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

  sendMessage(message: any): void {
    if (this.socket && this.socket.readyState === WebSocket.OPEN) {
      this.socket.send(message);
    }
  }

  onMessageReceived(callback: (msg: any) => void): void {
    if (this.socket) {
      this.socket.onmessage = event => {
        callback(event.data);
      };
    }
  }

  // Новый метод для отправки сообщения в текущий диалог
  sendMessageToCurrentDialog(message: any): void {
    this.sendMessage(message);
  }
}
