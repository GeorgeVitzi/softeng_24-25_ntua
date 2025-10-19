# SE2402 - CLI Tool for Toll Station Management

Το **SE2402** είναι ένα εργαλείο γραμμής εντολών (CLI) που επιτρέπει τη διαχείριση και την ανάλυση δεδομένων διοδίων μέσω REST API.

---

## 🔧 Εγκατάσταση & Εκτέλεση

1. **Δώσε εκτελέσιμα δικαιώματα στο script**:
   ```bash
   chmod +x se2402
   
2. **Πρόσθεσε το script στη μεταβλητή PATH:**:
   export PATH=$PATH:$(pwd)

3. **Εκτέλεση του CLI:**:
   se2402 [scope] [options]


📌 Διαθέσιμες Εντολές (Scopes)

Scope	Περιγραφή
healthcheck	Έλεγχος κατάστασης του συστήματος
resetpasses	Διαγραφή όλων των περασμάτων
resetstations	Διαγραφή όλων των σταθμών διοδίων
tollstationpasses	Προβολή διελεύσεων σε συγκεκριμένο σταθμό
passanalysis	Ανάλυση διελεύσεων μεταξύ σταθμών
passescost	Υπολογισμός κόστους διελεύσεων
chargesby	Ανάλυση χρεώσεων από πάροχο
admin	Διαχειριστικές λειτουργίες

🏗 Χρήση

🔹 Healthcheck
se2402 healthcheck --format csv
se2402 healthcheck --format json
Επιστρέφει την κατάσταση του συστήματος σε JSON ή CSV.

🔹 Διαγραφή Δεδομένων
se2402 resetpasses --format csv
se2402 resetstations --format json
Επαναφέρει τα δεδομένα στην αρχική τους κατάσταση και επιστρέφει μήνυμα επιτυχίας ή σφάλματος σε CSV ή JSON.

🔹 Προβολή Διελεύσεων σε Σταθμό
se2402 tollstationpasses --station ΧΧ01 --from YYYYMMDD --to YYYYMMDD --format csv
se2402 tollstationpasses --station ΧΧ01 --from YYYYMMDD --to YYYYMMDD --format json
Επιστρέφει τις διελεύσεις στον σταθμό ΧΧ01 ανάμεσα σε ένα χρονικό διάστημα (όπου ΧΧ ένας σταθμός διοδίων) σε CSV ή JSON.

🔹 Ανάλυση Διελεύσεων
se2402 passanalysis --stationop ΧΧ01 --tagop ΧΧ02 --from YYYYMMDD --to YYYYMMDD --format csv
se2402 passanalysis --stationop ΧΧ01 --tagop ΧΧ02 --from YYYYMMDD --to YYYYMMDD --format json
Αναλύει διελεύσεις μεταξύ των παρόχων ΧΧ01 και ΧΧ02 σε ένα χρονικό διάστημα σε CSV ή JSON.

🔹 Κόστος Διελεύσεων
se2402 passescost --stationop ΧΧ01 --tagop ΧΧ02 --from YYYYMMDD --to YYYYMMDD --format csv
se2402 passescost --stationop ΧΧ01 --tagop ΧΧ02 --from YYYYMMDD --to YYYYMMDD --format json
Υπολογίζει το κόστος διελεύσεων μεταξύ των παρόχων ΧΧ01 και ΧΧ02 σε ένα χρονικό διάστημα σε CSV ή JSON.

🔹 Ανάλυση Χρεώσεων από Πάροχο
se2402 chargesby --opid ΧΧ01 --from YYYYMMDD --to YYYYMMDD --format csv
se2402 chargesby --opid ΧΧ01 --from YYYYMMDD --to YYYYMMDD --format json
Επιστρέφει ανάλυση των χρεώσεων από τον πάροχο ΧΧ01 σε ένα χρονικό διάστημα σε CSV ή JSON.

🔹 Διαχειριστικές Λειτουργίες (Admin)
✅ Προσθήκη νέων περασμάτων
se2402 admin --addpasses --source passes02.csv --format csv
Προσθέτει νέες διελεύσεις από το αρχείο passes02.csv.

📁 Μορφές Εξόδου
Οι απαντήσεις αποθηκεύονται σε αρχεία .csv ή .json στον τρέχοντα κατάλογο.

❓ Υποστήριξη
Αν αντιμετωπίσετε προβλήματα, ελέγξτε το stderr ή την έξοδο JSON για λεπτομέρειες.
Για τεχνική υποστήριξη, επικοινωνήστε με τον διαχειριστή του συστήματος.
