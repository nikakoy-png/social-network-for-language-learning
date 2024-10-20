import {Component, OnInit, ElementRef, ViewChild, AfterViewChecked} from '@angular/core';
import {SocketDialogsListService} from "../socket-dialogs-list.service";
import {ActivatedRoute, Router} from "@angular/router";
import {environment} from "../../environments/environment";
import {CookieService} from 'ngx-cookie-service';
import {ApiService} from "../../api.service";
import {SocketDialogService} from "../socket-dialog.service";
import {MatDialog} from "@angular/material/dialog";
import {EditMessageDialogComponent} from "../edit-message-dialog/edit-message-dialog.component";
import {ShowFeedbackDialogComponent} from "../show-feedback-dialog/show-feedback-dialog.component";
import {CreateComplaintComponent} from "../create-complaint/create-complaint.component";

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit, AfterViewChecked {
  messageToSend: string = ''; // Переменная для хранения введенного сообщения
  socketDialogsListUrl = '';
  dialogs: any[] = [];
  currentlyDialog: any;
  newMessage: string = '';
  currentUser: any;
  messagesCurrentlyDialog: any[] = [];
  selfUserId: string = '';
  showAssistanceBlock: boolean = false;
  dialogSelected = false;
  loading: boolean = true;
  GPTAnswerHelpUnderstanding: any;
  TextAntwortGPT!: string;

  @ViewChild('messagesContainer') private messagesContainer!: ElementRef;
  showMenu: boolean = false;

  constructor(
    private socketService: SocketDialogsListService,
    private socketDialogService: SocketDialogService,
    private cookieService: CookieService,
    private apiService: ApiService,
    private dialog: MatDialog,
    private route: ActivatedRoute,
  ) {
  }

  ngOnInit(): void {
    this.loading = false;
    this.apiService.getProfile(this.cookieService.get("token")).subscribe(
      (user: any) => {
        this.currentUser = user;
        this.selfUserId = user.id;
      },
      error => {
        console.error('Error fetching user data:', error);
      }
    );
    this.socketDialogsListUrl = `${environment.SocketDialogsListUrl}dialogs/`;

    this.socketService.connectToSocketServer(this.socketDialogsListUrl);

    this.socketService.onMessageReceived((msg: any) => {
      const parsedMsg = JSON.parse(msg);
      console.log(parsedMsg)
      if (parsedMsg) {
        if (parsedMsg.type === 'UPDATE_DIALOG_LIST') {
          if (Array.isArray(parsedMsg.data)) {
            parsedMsg.data.forEach((newDialog: { dialog_id: any; last_message: any; unread_messages: any; }) => {
              const existingDialogIndex = this.dialogs.findIndex(dialog => dialog.dialog_id === newDialog.dialog_id);
              if (existingDialogIndex !== -1) {
                this.dialogs[existingDialogIndex].last_message = newDialog.last_message;
                this.dialogs[existingDialogIndex].unread_messages = newDialog.unread_messages;
                if (this.dialogs[existingDialogIndex].dialog_id === this.currentlyDialog.dialog_id) {
                  this.dialogs[existingDialogIndex].unread_messages = 0;
                }
              } else {
                this.dialogs.push(newDialog);
              }
            });
            this.dialogs = this.dialogs.filter(existingDialog => {
              return parsedMsg.data.some((newDialog: {
                dialog_id: any;
              }) => newDialog.dialog_id === existingDialog.dialog_id);
            });
          } else {
            const dialog = parsedMsg.data;
            const existingDialog = this.dialogs.find(d => d.dialog_id === dialog.dialog_id);
            if (existingDialog) {
              existingDialog.last_message = dialog.last_message;
              existingDialog.unread_messages = dialog.unread_messages;
            } else {
              this.dialogs.push(dialog);
            }
          }
        } else {
          this.dialogs = parsedMsg;
        }

        this.dialogs.sort((a, b) => {
          const dateA = a.last_message.send_date === "None" ? new Date(0) : new Date(a.last_message.send_date);
          const dateB = b.last_message.send_date === "None" ? new Date(0) : new Date(b.last_message.send_date);
          return dateB.getTime() - dateA.getTime();
        });


        this.dialogs.forEach(dialog => {
          if (!dialog.interlocutor) {
            this.apiService.getUserById(dialog.companion_id, this.cookieService.get("token")).subscribe(
              (user: any) => {
                dialog.interlocutor = user;
                dialog.interlocutor.photo = `${environment.apiGateWayUrl}user_service${dialog.interlocutor.photo}`;
              },
              error => {
                console.error('Error fetching user data:', error);
                console.error(dialog);
              }
            );
          }
        });

        this.loading = true;
        this.route.queryParams.subscribe(params => {
          const dialogId = params['dialogId'];
          if (dialogId) {
            const selectedDialog = this.dialogs.find(dialog => dialog.dialog_id === parseInt(dialogId));
            if (selectedDialog) {
              this.selectDialog(selectedDialog);
            } else {
              console.error('Dialog with id ' + dialogId + ' not found');
            }
          }
        });
      }
    });


    this.socketDialogService.onMessageReceived((msg: any) => {
      const parsedMsg = JSON.parse(msg);
      console.log(parsedMsg)
      if (parsedMsg.type === 'FEEDBACK') {
        this.handleFeedback(parsedMsg.message);
      }
    });

    this.socketDialogService.onMessageReceived((msg: any) => {
      const parsedMsg = JSON.parse(msg);
      console.log(parsedMsg)
      if (parsedMsg.type === 'DELETE') {
        console.log(parsedMsg.message.message_id)
        console.log(parsedMsg.message)
        this.messagesCurrentlyDialog = this.messagesCurrentlyDialog.filter(message => message.message.id !== parsedMsg.message.message_id);
      }
    });
  }

  getMessageClasses(messageSenderId: string): string {
    return messageSenderId === this.selfUserId ? 'outgoing' : 'incoming';
  }

  selectDialog(dialog: any): void {
    if (this.currentlyDialog) {
      this.currentlyDialog = null;
      this.messagesCurrentlyDialog = [];
      this.socketDialogService.disconnectFromSocketServer()
    }

    this.currentlyDialog = dialog;
    this.currentlyDialog.unread_messages = 0;

    this.socketDialogService.connectToSocketServer(`${environment.SocketDialogUrl}dialog/${dialog.dialog_id}/`);
    this.socketDialogService.onMessageReceived((msg: any) => {
      const parsedMsg = JSON.parse(msg);
      if (parsedMsg.type === 'MESSAGE') {
        if (parsedMsg.message.feedback != null) {
          this.messagesCurrentlyDialog.push(parsedMsg);
          this.handleFeedback(parsedMsg.message);
          console.log(this.messagesCurrentlyDialog)
          return;
        }
        this.messagesCurrentlyDialog.push(parsedMsg);
      }
      if (parsedMsg.type === 'FEEDBACK') {
        const index = this.messagesCurrentlyDialog.findIndex(message => message.message.id === parsedMsg.message.id);
        if (index !== -1) {
          this.messagesCurrentlyDialog[index] = parsedMsg;
        }
        this.handleFeedback(parsedMsg.message);
      }
    });
    this.dialogSelected = true;
  }

  showEditIcon_(message: any): boolean {
    return message.sender_id !== this.selfUserId;
  }

  showDeleteIcon_(message: any): boolean {
    return message.sender_id === this.selfUserId;
  }

  deleteMsg(message_id: number): void {
    this.messagesCurrentlyDialog = this.messagesCurrentlyDialog.filter(message => message.message.id !== message_id);
    const messageData = {
      type: 'DELETE',
      message_id: message_id
    };

    this.socketDialogService.sendMessageToCurrentDialog(JSON.stringify(messageData));
  }

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  scrollToBottom(): void {
    try {
      this.messagesContainer.nativeElement.scrollTop = this.messagesContainer.nativeElement.scrollHeight;
    } catch (err) {
    }
  };

  onScroll(event: Event): void {
    const container = this.messagesContainer.nativeElement;
    if (container.scrollTop === 0) {
      console.log('Reached top of container');
    }
    event.stopPropagation();
  }

  handleFeedback(feedbackMessage: any): void {
    const messageToUpdate = this.messagesCurrentlyDialog.find(message => message.message.id === feedbackMessage.id);
    if (messageToUpdate) {
      messageToUpdate.isFeedback = true;
    }
  }

  openEditDialog(messageText: string, messageId: string): void {
    const dialogRef = this.dialog.open(EditMessageDialogComponent, {
      width: '400px',
      data: {messageText: messageText, messageId: messageId}
    });

    dialogRef.afterClosed().subscribe((result: any) => {
      if (result) {
        const messageData = {
          type: 'FEEDBACK',
          message: result.editedMessage,
          description: result.editedDescription,
          message_id: messageId
        };

        this.socketDialogService.sendMessageToCurrentDialog(JSON.stringify(messageData));
      }
    });
  }

  openShowDialog(messageText: string, description: string): void {
    this.dialog.open(ShowFeedbackDialogComponent, {
      width: '400px',
      data: {messageText: messageText, description: description}
    });
  }

  sendMessageFromHelp(text: string): void {
    const messageData = {
      type: 'MESSAGE',
      message: text
    };

    this.socketDialogService.sendMessageToCurrentDialog(JSON.stringify(messageData));
    this.toggleAssistanceBlock()
  }

  sendMessage(): void {
    if (this.newMessage.trim() === '') return;

    const messageData = {
      type: 'MESSAGE',
      message: this.newMessage
    };

    this.socketDialogService.sendMessageToCurrentDialog(JSON.stringify(messageData));

    this.newMessage = '';
  }

  toggleAssistanceBlock() {
    this.showAssistanceBlock = !this.showAssistanceBlock;
    this.GPTAnswerHelpUnderstanding = null;
    this.messageToSend = '';
  }

  sendRequestToHelpUnderstanding() {
    const messages = JSON.stringify(this.messagesCurrentlyDialog.slice(-10).map(item => item.message));
    const languages = JSON.stringify(this.currentUser.languages);

    // Находим язык с самым высоким уровнем
    let highestLanguage: {
      id: number,
      language: {
        id: number,
        title: string
      },
      proficiency_level: string,
      is_learning: boolean
    } | null = null;
    this.currentUser.languages.forEach((language: {
      id: number;
      language: { id: number; title: string; };
      proficiency_level: string;
      is_learning: boolean;
    } | null) => {
      // @ts-ignore
      if (!highestLanguage || language.proficiency_level > highestLanguage.proficiency_level) {
        highestLanguage = language;
      }
    });

    // @ts-ignore
    this.apiService.getHelpWithUnderstanding(messages, highestLanguage.language.title).subscribe(
      (answer: any) => {
        console.log(answer)
        this.GPTAnswerHelpUnderstanding = answer;
      },
      error => {
        console.error('Error fetching user data:', error);
      }
    );
  }


  toggleMenu() {
    this.showMenu = !this.showMenu;
  }

  complain(user_id: number, dialog_id: number) {
    const dialogRef = this.dialog.open(CreateComplaintComponent, {
      width: '400px',
      data: {user_id: user_id, dialog_id: dialog_id}
    });

    dialogRef.afterClosed().subscribe((result: any) => {
      if (result) {
        this.apiService.createComplaint(result.user_id, result.dialog_id, result.description).subscribe(
          (result: any) => {
            console.log(result);
          },
          error => {
            console.error('Error fetching user data:', error);
          }
        );
      }
    });
  }

  delete(dialog_id: number, user_id: number) {
    this.apiService.deleteDialog(this.cookieService.get("token"), dialog_id, user_id).subscribe(
      (result: any) => {
        console.log(result);
        this.dialogSelected = false;
        this.currentlyDialog = null;
      },
      error => {
        console.log(error);
      }
    );
  }

  sendRequestToHelpUnderstandingTEXT() {
    let highestLanguage: {
      id: number,
      language: {
        id: number,
        title: string
      },
      proficiency_level: string,
      is_learning: boolean
    } | null = null;
    this.currentUser.languages.forEach((language: {
      id: number;
      language: { id: number; title: string; };
      proficiency_level: string;
      is_learning: boolean;
    } | null) => {
      // @ts-ignore
      if (!highestLanguage || language.proficiency_level > highestLanguage.proficiency_level) {
        highestLanguage = language;
      }
    });

    // @ts-ignore
    this.apiService.sendRequestToHelpUnderstanding(this.cookieService.get("token"), this.messageToSend, highestLanguage.language.title).subscribe(
      (response: any) => {
        console.log(response);
        this.TextAntwortGPT = response.data
      },
      error => {
        console.error('Error sending request:', error);
      }
    );
  }

}
