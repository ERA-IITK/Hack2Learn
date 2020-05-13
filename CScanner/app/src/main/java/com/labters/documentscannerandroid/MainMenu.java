package com.labters.documentscannerandroid;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.ImageButton;

import com.google.firebase.auth.FirebaseAuth;

public class MainMenu extends AppCompatActivity {
    ImageButton top_left,top_right,bottom_repeat;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main_menu);

        top_left = (ImageButton)findViewById(R.id.button_topleft);
        top_left.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(getApplicationContext(),MainActivity.class);
                startActivity(i);
            }
        });
        top_right = (ImageButton)findViewById(R.id.button_topright);
        top_right.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(getApplicationContext(),barcode.class);
                startActivity(i);
            }
        });
        bottom_repeat = (ImageButton)findViewById(R.id.button_repeat);
        bottom_repeat.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent i = new Intent(getApplicationContext(),text_recog.class);
                startActivity(i);
            }
        });
    }
    public void logout(View view) {
        FirebaseAuth.getInstance().signOut();//logout
        startActivity(new Intent(getApplicationContext(),Register.class));
        finish();
    }
}
