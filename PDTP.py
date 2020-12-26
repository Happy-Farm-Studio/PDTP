import socket
import json
import re

class Socket():
    def __init__(self,Type,Encode,Decode):
        self.TCP_Serve = 0
        self.Type = Type
        self.Encode = Encode
        self.Decode = Decode
        
        if(Type == "TCP"):
            self.TCP_Socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            
        if(Type == "UDP"):
            self.UDP_Socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            
    def SetUDP(self,Target_IP,Target_Port):
        Type = self.Type
            
        if(Type == "TCP"):
            print("TCP Doesn't Support This Function")
            
        if(Type == "UDP"):
            self.Target_IP = Target_IP
            self.Target_Port = Target_Port
            
    def Bind(self,Host_IP,Host_Port):
        Type = self.Type
        
        if(Type == "TCP"):
            TCP_Socket = self.TCP_Socket
            TCP_Socket.bind((Host_IP,Host_Port))
            
        if(Type == "UDP"):
            UDP_Socket = self.UDP_Socket
            UDP_Socket.bind((Host_IP,Host_Port))
            
    def Listen(self,Max_Waiting_Conn):
        Type = self.Type
        
        if(Type == "TCP"):
            TCP_Socket = self.TCP_Socket
            TCP_Socket.listen(Max_Waiting_Conn)
            
        if(Type == "UDP"):
            print("UDP Doesn't Support This Function")
            
    def Accept(self):
        Type = self.Type
        
        if(Type == "TCP"):
            self.TCP_Serve = 1
            
            TCP_Socket = self.TCP_Socket
            TCP_User_Socket,TCP_User_Addr = TCP_Socket.accept()
            
            self.TCP_User_Socket = TCP_User_Socket
            return TCP_User_Addr
            
        if(Type == "UDP"):
            print("UDP Doesn't Support This Function")

    def Conn(self,Serve_IP,Serve_Port):
        Type = self.Type
        
        if(Type == "TCP"):
            TCP_Socket = self.TCP_Socket
            TCP_Socket.connect((Serve_IP,Serve_Port))
            
        if(Type == "UDP"):
            print("UDP Doesn't Support This Function")
            
    def Send(self,Data):
        Type = self.Type
        Encode = self.Encode

        if(Encode != ""):
            Data = Data.encode(Encode)
        
        if(Type == "TCP"):
            TCP_Serve = self.TCP_Serve
            
            if(TCP_Serve == 0):
                TCP_Socket = self.TCP_Socket
                TCP_Socket.send(Data)
            else:
                TCP_User_Socket = self.TCP_User_Socket
                TCP_User_Socket.send(Data)
                
        if(Type == "UDP"):
            Target_IP = self.Target_IP
            Target_Port = self.Target_Port
                
            UDP_Socket = self.UDP_Socket
            UDP_Socket.sendto(Data,(Target_IP,Target_Port))
            
    def Recv(self,Data_Size):
         Type = self.Type
         Decode = self.Decode
         
         if(Type == "TCP"):
             TCP_Serve = self.TCP_Serve
             
             if(TCP_Serve == 0):
                 TCP_Socket = self.TCP_Socket
                 
                 if(Decode == ""):
                    return TCP_Socket.recv(Data_Size)
                 else:
                    return TCP_Socket.recv(Data_Size).decode(Decode)
                
             else:
                 TCP_User_Socket = self.TCP_User_Socket
                 
                 if(Decode == ""):
                    return TCP_User_Socket.recv(Data_Size)
                 else:
                    return TCP_User_Socket.recv(Data_Size).decode(Decode)
                    
         if(Type == "UDP"):
             Target_IP = self.Target_IP
             Target_Port = self.Target_Port
             UDP_Socket = self.UDP_Socket
             return UDP_Socket.recv(Data_Size).decode(Encoding)
             
    def Close(self):
         Type = self.Type
         
         if(Type == "TCP"):
             TCP_Socket = self.TCP_Socket

         if(Type == "UDP"):
             UDP_Socket = self.UDP_Socket
             UDP_Socket.close()


class Web():
    def __init__(self):
        self.Web_Socket = Socket("TCP","GBK")
        
    def SetConfig(self,ConfigAddr):
        if(ConfigAddr == 0):
            ConfigAddr = "PDTPWebConfig.json"
        
        with open(ConfigAddr,"r") as RC:
            Config = json.load(RC)
            
        self.Type = Config["Type"]
        self.Config = Config

    def UserSet(self,Serve_IP,Serve_Port):
        Type = self.Type
        
        if(Type == "Serve"):
            print("User Type Doesn't Support This Function")
            
        if(Type == "User"):
            self.Serve_IP = Serve_IP
            self.Serve_Port = Serve_Port
        
    def Start(self):
        Type = self.Type
        Config = self.Config
        Web_Socket = self.Web_Socket
        
        if(Type == "Serve"):
            Serve_Addr = Config["Addr"]
            Serve_Conn = Config["Conn"]
            
            Host_IP = Serve_Addr["Host_IP"]
            Host_Port = Serve_Addr["Host_Port"]
            Max_Connection = Serve_Conn["Max_Connection"]
            
            Serve_Socket = Web_Socket
            Serve_Socket.Bind(Host_IP,Host_Port)
            Serve_Socket.Listen(Max_Connection)
            
            while(True):
                User_Addr = Serve_Socket.Accept()
                User_Request = Serve_Socket.Recv(1024).splitlines()
                print(User_Request)
        
        if(Type == "User"):
            Serve_IP = self.Serve_IP
            Serve_Port = self.Serve_Port
            
            User_Addr = Config["Addr"]
            
            Host_IP = User_Addr["Host_IP"]
            Host_Port = User_Addr["Host_Port"]
            
            User_Socket = Web_Socket
            User_Socket.Bind(Host_IP,Host_Port)
            User_Socket.Conn(Serve_IP,Serve_Port)

    def Request(self,Data):
        Type = self.Type
        
        if(Type == "Serve"):
            print("Serve Type Doesn't Support This Function")

        if(Type == "User"):
            User_Socket = self.Web_Socket
            User_Socket.Send(Data)

