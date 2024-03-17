package cn.kalud.client.test;


import net.minecraft.client.Minecraft;
import net.minecraft.client.entity.EntityPlayerSP;
import net.minecraft.entity.player.EntityPlayer;
import net.minecraft.entity.player.EntityPlayerMP;
import net.minecraft.world.World;
import net.minecraft.world.WorldSettings;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;


/**
 * @author Kalud
 * @website pixelskider.github.io/
 * @since 2023/12/09
 */
public class Net {

    //数据
    int health;
    EntityPlayer player = null;
    //本地服务器
    ServerSocket serverSocket = null;
    //等客户端
    Socket socket = null;
    //写入数据
    BufferedWriter bw  = null;

    public void Start() throws IOException {
        if (Minecraft.getMinecraft() != null){
            player = Minecraft.getMinecraft().thePlayer;
        }

        serverSocket = new ServerSocket(1111);
        socket = serverSocket.accept();
        bw = new BufferedWriter(new OutputStreamWriter(socket.getOutputStream()));

        //发送数据
        new Thread(() ->{
            while (true){
                try {
                    if (player != null ){
                        health = (int)player.getHealth();
                    }else {
                        health = 0;
                        player = Minecraft.getMinecraft().thePlayer;
                    }
                    bw.write(health);
                    bw.flush();
                    System.out.println(health);
                    Thread.sleep(1000);
                } catch (InterruptedException | IOException e) {
                    throw new RuntimeException(e);
                }
            }
        }).start();
    }

    public void Stop() throws IOException {
        serverSocket.close();
        socket.close();
        bw.close();
    }
}
