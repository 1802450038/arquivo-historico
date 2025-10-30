<?php

namespace App\Http\Controllers;

use App\Models\Post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    public function index(){
        $posts = Post::latest()->with('book')->get();
        
        return view('index', ['posts'=> $posts]);
    }

    public function show($id){
        $post = Post::with('book')->find($id);
        // $post->file = $post->book->book_pdf_file;
        return view('bookDetails', ['post'=> $post]);
    }
}
