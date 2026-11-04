"""
Práctica 3: Modelado y control del sistema musculoesquelético

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Garcia Grijalva Armando
Número de control: 23212195
Correo institucional: L23212195@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
import numpy as np
import control as ctrl
import matplotlib.pyplot as plt

#Datos Generales de la Simulacion
x0,t0,tend,dt,w,h = 0,0,10,1E-3,7,3.5
N = round(tend/dt) + 1
t = np.linspace(t0,tend,N)
u = np.zeros(N)
u[round(1/dt):round(2/dt)] = 1

#Componentes Circuito
R,Cs,Cp,a = 100, 10E-6, 100E-6, 0.25
Rcaso = 10E3
sys = ctrl.tf([R*Cs, 1-a],[R*(Cp+Cs), 1])
sysCaso = ctrl.tf([R*Cs, 1-a],[Rcaso*(Cp+Cs), 1])
sysT = ctrl.tf([Rcaso*Cs, 1-a],[Rcaso*(Cp+Cs), 1])

#Componentes del controlador
kP,kI,kD = 0.013239, 68547.1067, 0
PID = ctrl.tf([kD,kP,kI],[1,0])

#Sistema de control en lazo cerrado
sysPID = ctrl.feedback(ctrl.series(PID,sysT),1,sign=-1)

#Respuestas
_,Fsx = ctrl.forced_response(sys,t,u,x0)
_,FsY = ctrl.forced_response(sysCaso,t,u,x0)
_,PIDu = ctrl.forced_response(sysPID,t,Fsx,x0)

# Colores
clr1 = np.array([247, 0, 99])/255;
clr2 = np.array([255, 203, 86])/255;
clr3 = np.array([35, 145, 255])/255;
clr4 = np.array([114, 142, 109])/255;

fg = plt.figure(1)
fg.set_size_inches(w,h)
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Times New Roman'
plt.plot(t,u,'-',color=clr1,label='F(t)')
plt.plot(t,Fsx,'-',color=clr2,label='Fs(t): Control')
plt.plot(t,FsY,'-',color=clr3,label='Fs(t): Caso')
plt.plot(t,PIDu,'--',linewidth=2.5,color=clr4,label='PID: Tratamiento')
plt.xlim(-0.25,10); plt.xticks(np.arange(0,11,1))
plt.ylim(0,1.2); plt.yticks(np.arange(0,1.3,0.1))
plt.xlabel('t [s]')
plt.ylabel('Fi(t) [V]')
plt.legend(bbox_to_anchor=(0.5, 1.12), loc='center', ncol=4)
fg.savefig('Señal_python.pdf', bbox_inches='tight')
plt.show()