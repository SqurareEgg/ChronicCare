using ChronicCare.Components;
using ChronicCare.Data;
using ChronicCare.Services;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddRazorComponents()
    .AddInteractiveServerComponents();

// 데이터 레이어
builder.Services.AddSingleton<DatabaseHelper>();
builder.Services.AddScoped<PatientRepository>();
builder.Services.AddScoped<MeasurementRepository>();
builder.Services.AddScoped<AlertRepository>();
builder.Services.AddScoped<StatisticsRepository>();

// 인증 서비스 (Scoped = 사용자 세션마다 독립)
builder.Services.AddScoped<AuthService>();

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error", createScopeForErrors: true);
    app.UseHsts();
}

app.UseStatusCodePagesWithReExecute("/not-found", createScopeForStatusCodePages: true);
if (!app.Environment.IsDevelopment())
    app.UseHttpsRedirection();
app.UseAntiforgery();

app.MapStaticAssets();
app.MapRazorComponents<App>()
    .AddInteractiveServerRenderMode();

app.Run();
