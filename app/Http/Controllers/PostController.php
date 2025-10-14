<?php

namespace App\Http\Controllers;

use App\Models\post;
use Illuminate\Http\Request;

class PostController extends Controller
{
    public function index(){
        $posts = post::latest()->get();

        return view('index', ['posts'=> $posts]);
    }

    public function show($id){
        $post = post::find($id);

        return view('bookDetails', ['post'=> $post]);
    }
}
