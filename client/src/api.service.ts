import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from "@angular/common/http";
import {Observable} from "rxjs";
import {environment} from "./environments/environment";
import {User} from "./interfaces/user.interfaces";
import {LoginDTO} from "./models/login.dto";

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  constructor(private http: HttpClient) {
  }

  register(user_data: User, imageFile: File): Observable<any> {
    const formData = new FormData();
    formData.append('email', user_data.email);
    formData.append('gender', user_data.gender);
    formData.append('birth_date', user_data.birthday);
    formData.append('username', user_data.username);
    formData.append('first_name', user_data.first_name);
    formData.append('last_name', user_data.last_name);
    formData.append('phone', user_data.phone);
    formData.append('password', user_data.password);
    formData.append('password_confirm', user_data.password_confirm);

    if (imageFile) {
      formData.append('photo', imageFile);
    }

    return this.http.post(`${environment.apiGateWayUrl}user_service/register/`, formData);
  }

  login(user_data: LoginDTO): Observable<any> {
    return this.http.post(`${environment.apiGateWayUrl}user_service/login/`, user_data)
  }

  getUserById(user_id: number, jwtToken: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });
    return this.http.get(`${environment.apiGateWayUrl}user_service/get_user_by_id/${user_id}/`, {headers});
  }

  getProfile(jwtToken: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });
    return this.http.get(`${environment.apiGateWayUrl}user_service/user/profile/`, {headers});
  }

  GetSuitableUsers(jwtToken: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });
    return this.http.get(`${environment.apiGateWayUrl}user_service/get_suitable_users/`, {headers})
  }

  createDialog(user_id_1: number, user_id_2: number): Observable<any> {
    return this.http.post(`${environment.apiGateWayUrl}communication_service/create_dialog/`, {"user_ids": [user_id_1, user_id_2]})
  }

  getHelpWithUnderstanding(messages: any, languages: any): Observable<any> {
    console.log(messages)
    console.log(languages)
    return this.http.post(`${environment.apiGateWayUrl}gpt_service/help_with_understanding/`, {
      "messages": messages,
      "language_user": languages
    })
  }

  createComplaint(user_id: number, dialog_id: number, description: string): Observable<any> {
    return this.http.post(`${environment.apiGateWayUrl}communication_service/create_complaint/`, {
      "user_id": user_id,
      "dialog_id": dialog_id,
      "description": description
    })
  }

  updateDataUserProfile(jwtToken: string, user_data: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    const updatedUserData = {...user_data};

    delete updatedUserData.photo;
    delete updatedUserData.languages;
    console.log(updatedUserData);

    return this.http.patch(`${environment.apiGateWayUrl}user_service/user/update_profile/`,
      {user_data: updatedUserData},
      {headers}
    );
  }

  deleteLanguageUser(jwtToken: string, language_id: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.delete(`${environment.apiGateWayUrl}user_service/user/delete_language/${language_id}/`, {headers})
  }

  getListLanguages(jwtToken: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.get(`${environment.apiGateWayUrl}user_service/languages/`)
  }

  addLanguageUser(jwtToken: string, user_language: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.patch(`${environment.apiGateWayUrl}user_service/user/add_language/`, {user_language},
      {headers})
  }

  updPhotoProfileUser(jwtToken: string, formData: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.patch(`${environment.apiGateWayUrl}user_service/user/update_profile/`, formData,
      {headers})
  }

  sendRequestToHelpUnderstanding(jwtToken: string, message: string, language_user: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.post(`${environment.apiGateWayUrl}gpt_service/get_text_response/`,
      {"messages": message, "language_user": language_user}, {headers});
  }

  deleteDialog(jwtToken: string, dialog_id: number, user_id: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.delete(`${environment.apiGateWayUrl}communication_service/delete_dialog/${dialog_id}/${user_id}/`,
      {headers});
  }

  login_admin(admin: LoginDTO): Observable<any> {
    return this.http.post(`${environment.apiGateWayUrl}admin_service/login/`, admin);
  }

  getListUsersForAdmin(jwtToken: string, page_number: number = 1, page_size: number = 20): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.get(`${environment.apiGateWayUrl}admin_service/get_list_users/${page_number}/${page_size}/`,
      {headers});
  }

  getStatisticUserForAdmin(jwtToken: string, user_id: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.get(`${environment.apiGateWayUrl}communication_service/get_user_statistic/${user_id}/`,
      {headers});
  }

  getPerformances(jwtToken: string, user_id: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.get(`${environment.apiGateWayUrl}admin_service/get_perfomances/${user_id}/`, {headers});
  }

  addPerformance(jwtToken: string, performance: any): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.post(`${environment.apiGateWayUrl}admin_service/add_performances/`, performance,
      {headers});
  }

  getCountPerformances(jwtToken: string, user_id: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.get(`${environment.apiGateWayUrl}admin_service/get_count_perfomances/${user_id}/`, {headers});
  }

  getUserForAdminUsername(jwtToken: string, username: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });
    return this.http.get(`${environment.apiGateWayUrl}user_service/get_user_for_admin/${username}/`, {headers});
  }

  getComplaints(jwtToken: string, page_number: number = 1, page_size: number = 20, is_answer = false): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });
    return this.http.get(`${environment.apiGateWayUrl}communication_service/get_complaints/${page_number}/${page_size}/${is_answer}/`, {headers});
  }

  getDetailsDialogs(jwtToken: string, dialog_id: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.get(`${environment.apiGateWayUrl}communication_service/get_details_dialogs/${dialog_id}/`, {headers});
  }

  getComplaintsByUserID(jwtToken: string, user_id: string, is_answer = false): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });
    return this.http.get(`${environment.apiGateWayUrl}communication_service/get_complaints_by_user_id/${user_id}/${is_answer}/`, {headers});
  }

  getListDialogsUserForAdmin(jwtToken: string, user_id: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.get(`${environment.apiGateWayUrl}communication_service/get_list_dialogs_for_admin/${user_id}/`, {headers});
  }

  getListMessagesUserForAdmin(jwtToken: string, dialog_id: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.get(`${environment.apiGateWayUrl}communication_service/get_list_messages_for_admin/${dialog_id}/`, {headers});
  }

  getAdminData(jwtToken: string, admin_id: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.get(`${environment.apiGateWayUrl}admin_service/get_admin_data/${admin_id}/`, {headers});
  }

  updateActiveStatus(jwtToken: string, user_id: number): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.patch(`${environment.apiGateWayUrl}user_service/update_user_status_for_admin/${user_id}/`, {}, {headers});
  }

  setResolution(jwtToken: string, complaint: number, resolution_text: string): Observable<any> {
    const headers = new HttpHeaders({
      'Authorization': `Bearer ${jwtToken}`
    });

    return this.http.post(`${environment.apiGateWayUrl}communication_service/set_resolution_on_complaint/${complaint}/`, {resolution: resolution_text}, {headers});
  }
}
