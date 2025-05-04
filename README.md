# VERDIKTIA – Inteligencia Artificial para la Internacionalización Estratégica

**VERDIKTIA** es un sistema inteligente basado en modelos de lenguaje generativo y arquitectura deliberativa que guía a pequeñas y medianas empresas en el diseño de su estrategia de internacionalización. Combina razonamiento guiado, recomendaciones adaptativas y planes de expansión según el modelo de Uppsala.

---

## 🚀 Características

- Diagnóstico estratégico basado en un Canvas inteligente.
- Generación automática de subpreguntas y razonamiento visual.
- Recomendaciones de adaptación a mercados objetivo.
- Ranking de países según perfil y pesos personalizados.
- Plan de entrada y escalado en mercados priorizados.
- Interfaz accesible construida con Streamlit.

---

## 📸 Capturas de pantalla

> (Añadir imágenes si se desea)

---

## 🧠 Fundamento teórico

Este MVP se basa en una arquitectura cognitiva de IA deliberativa descrita en los siguientes trabajos académicos:

- `Language, Code and Agency: Computation as an Epistemically Active Technology`
- `Inquiry-Based Cognitive Architectures`
- `El Código Deliberativo (v1.2)`
- `Del símbolo al protocolo: sentido y deliberación en la IA generativa`

---

## 🛠 Estructura del repositorio

verdiktia/
- ├── init.py
- ├── app.py # Punto de entrada principal
- ├── ui.py # Renderizado de inputs, canvas, grafo y resultados
- ├── data.py # Carga de datos de países y factores
- ├── logic.py # Lógica de ranking por pesos
- ├── inquiry.py # Generación de subpreguntas con IA
- ├── adaptation.py # Motor de recomendaciones adaptativas
- ├── expansion.py # Generación de plan de expansión internacional
- ├── config.yaml # Configuración de pesos por defecto
- └── requirements.txt # Dependencias del proyecto



#📦 Requisitos
- Python 3.9+
- Cuenta en OpenAI
- Conexión a internet
- graphviz instalado (puede requerir apt install graphviz en Linux)

#🤖 Créditos
- Desarrollado por @jftmames y colaboradores.
- Inspirado por la necesidad de herramientas accesibles de IA para la toma de decisiones estratégicas en entornos reales.


