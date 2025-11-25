from controller.turno_controller import TurnoController
from datetime import datetime, timedelta

def verify_filter():
    controller = TurnoController()
    
    # 1. Create a dummy turno for today
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    
    print(f"Testing filter for today: {today}")
    
    # We need valid IDs for patient and medico. 
    # Let's assume there are some from the seeder.
    pacientes = controller.listar_pacientes()
    medicos = controller.listar_medicos()
    estados = controller.listar_estados()
    
    if not pacientes or not medicos:
        print("Skipping test: No patients or medicos found.")
        return

    p_id = pacientes[0].id_paciente
    m_id = medicos[0].id_medico
    e_id = estados[0].id_estado
    
    # Create a turno
    try:
        # We need to find a valid time slot. This might be tricky without knowing the agenda.
        # Let's just try to filter existing ones if any, or try to insert one.
        # Actually, simpler: just list all turnos, pick one's date, and filter by that.
        
        turnos = controller.listar_turnos()
        if not turnos:
            print("No turnos found. Cannot verify filter with existing data.")
            # Try to create one? It requires agenda validation which is complex to mock here.
            return

        target_turno = turnos[0]
        target_date = target_turno.fecha
        
        print(f"Found turno with date: {target_date}")
        
        # Test 1: Filter including the date
        filtered = controller.filtrar_turnos(target_date, target_date)
        found = any(t.id_turno == target_turno.id_turno for t in filtered)
        print(f"Test 1 (Exact Date): {'PASSED' if found else 'FAILED'}")
        
        # Test 2: Filter excluding the date (past)
        past_date = "1990-01-01"
        filtered_past = controller.filtrar_turnos(past_date, past_date)
        found_past = any(t.id_turno == target_turno.id_turno for t in filtered_past)
        print(f"Test 2 (Past Date): {'PASSED' if not found_past else 'FAILED'}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    verify_filter()
