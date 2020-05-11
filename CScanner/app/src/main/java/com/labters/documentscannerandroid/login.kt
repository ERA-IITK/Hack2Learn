package com.labters.documentscannerandroid

import androidx.appcompat.app.AppCompatActivity

import android.content.Intent
import android.os.Bundle
import android.text.TextUtils
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast

import com.google.firebase.auth.FirebaseAuth

class login : AppCompatActivity() {

    internal lateinit var mEmail: EditText
    internal lateinit var mPassword: EditText
    internal lateinit var mLoginBtn: Button
    internal lateinit var mCreateBtn: TextView
    internal lateinit var progressBar: ProgressBar
    internal lateinit var fAuth: FirebaseAuth

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_login)

        mEmail = findViewById(R.id.Email)
        mPassword = findViewById(R.id.password)
        progressBar = findViewById(R.id.progressBar)
        fAuth = FirebaseAuth.getInstance()
        mLoginBtn = findViewById(R.id.loginBtn)
        mCreateBtn = findViewById(R.id.createText)

        mLoginBtn.setOnClickListener(View.OnClickListener {
            val email = mEmail.text.toString().trim { it <= ' ' }
            val password = mPassword.text.toString().trim { it <= ' ' }

            if (TextUtils.isEmpty(email)) {
                mEmail.error = "Email is Required."
                return@OnClickListener
            }

            if (TextUtils.isEmpty(password)) {
                mPassword.error = "Password is Required."
                return@OnClickListener
            }

            if (password.length < 6) {
                mPassword.error = "Password Must be >= 6 Characters"
                return@OnClickListener
            }

            progressBar.visibility = View.VISIBLE

            // authenticate the user

            fAuth.signInWithEmailAndPassword(email, password).addOnCompleteListener { task ->
                if (task.isSuccessful) {
                    Toast.makeText(this@login, "Logged in Successfully", Toast.LENGTH_SHORT).show()
                    startActivity(Intent(applicationContext, MainMenu::class.java))
                } else {
                    Toast.makeText(
                        this@login,
                        "Error ! " + task.exception!!.message,
                        Toast.LENGTH_SHORT
                    ).show()
                    progressBar.visibility = View.GONE
                }
            }
        })



        mCreateBtn.setOnClickListener {
            startActivity(
                Intent(
                    applicationContext,
                    Register::class.java
                )
            )
        }


    }
}
