import { Component, OnInit } from '@angular/core';
import { AppServiceService } from './app-service.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'iotians';

  constructor(private service : AppServiceService){

  }

  // public data!: Object;
  public data:any = []

  ngOnInit(){
    this.getDataFromAPI();
  }

  getDataFromAPI(){
    this.service.getData().subscribe((response)=>{
      this.data = response;
      console.log("Response from API:", response);
    }, (err)=>{
      console.log("Error:", err);
    })
  }

}
