package com.labters.documentscannerandroid

import androidx.appcompat.app.AppCompatActivity


import android.content.Intent
import android.os.Bundle
import android.text.TextUtils
import android.util.Log
import android.view.View
import android.widget.Button
import android.widget.EditText
import android.widget.ProgressBar
import android.widget.TextView
import android.widget.Toast

import com.google.firebase.auth.FirebaseAuth

import com.google.firebase.firestore.FirebaseFirestore


import java.util.HashMap


class Register : AppCompatActivity() {
    internal lateinit var mFullName: EditText
    internal lateinit var mEmail: EditText
    internal lateinit var mPassword: EditText
    internal lateinit var mRegisterBtn: Button
    internal lateinit var mLoginBtn: TextView
    internal lateinit var fAuth: FirebaseAuth
    internal lateinit var progressBar: ProgressBar
    internal lateinit var fStore: FirebaseFirestore
    internal lateinit var userID: String

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_register)

        mFullName = findViewById(R.id.fullName)
        mEmail = findViewById(R.id.Email)
        mPassword = findViewById(R.id.password)
        mRegisterBtn = findViewById(R.id.registerBtn)
        mLoginBtn = findViewById(R.id.createText)

        fAuth = FirebaseAuth.getInstance()
        fStore = FirebaseFirestore.getInstance()
        progressBar = findViewById(R.id.progressBar)

        if (fAuth.currentUser != null) {
            startActivity(Intent(applicationContext, MainActivity::class.java))
            finish()
        }


        mRegisterBtn.setOnClickListener(View.OnClickListener {
            val email = mEmail.text.toString().trim { it <= ' ' }
            val password = mPassword.text.toString().trim { it <= ' ' }
            val fullName = mFullName.text.toString()

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

            // register the user in firebase

            fAuth.createUserWithEmailAndPassword(email, password).addOnCompleteListener { task ->
                if (task.isSuccessful) {
                    Toast.makeText(this@Register, "User Created.", Toast.LENGTH_SHORT).show()
                    userID = fAuth.currentUser!!.uid
                    val documentReference = fStore.collection("users").document(userID)
                    val user = HashMap<String, Any>()
                    user["fName"] = fullName
                    user["email"] = email

                    documentReference.set(user).addOnSuccessListener {
                        Log.d(
                            TAG,
                            "onSuccess: user Profile is created for $userID"
                        )
                    }.addOnFailureListener { e -> Log.d(TAG, "onFailure: $e") }
                    startActivity(Intent(applicationContext, MainMenu::class.java))

                } else {
                    Toast.makeText(
                        this@Register,
                        "Error ! " + task.exception!!.message,
                        Toast.LENGTH_SHORT
                    ).show()
                    progressBar.visibility = View.GONE
                }
            }
        })



        mLoginBtn.setOnClickListener {
            startActivity(
                Intent(
                    applicationContext,
                    login::class.java
                )
            )
        }

    }

    companion object {
        val TAG = "TAG"
    }
}
