package com.springtutor.backend.config;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

// @Configuration: le dice a Spring que esta clase tiene configuración
@Configuration
public class WebConfig implements WebMvcConfigurer {

  @Override
  public void addCorsMappings(CorsRegistry registry) {
    registry.addMapping("/api/**") // aplica a todos los endpoints /api/
        .allowedOrigins("http://localhost:4200") // permite peticiones desde Angular
        .allowedMethods("GET", "POST", "PUT", "DELETE") // métodos permitidos
        .allowedHeaders("*"); // permite todos los headers
  }
}